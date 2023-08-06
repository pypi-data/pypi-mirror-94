# -*- coding: utf-8 -*-
""" Copyright 2020 Marco Arrigoni

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import numpy as np
import os
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
import h5py
from mpi4py import MPI

from clinamen.evpd.core.individual import Individual
from clinamen.evpd.core.population import Population
from clinamen.cmaes.evolution import (StrategyParameters, TerminationCriteria,
                                      CMAES, GpCMAES)
from clinamen.cmaes.fitness_calculators import *


class PopulationEvolver:
    """ Evolves a ``Population`` instance using the CMA-ES algorithm

    Parameters
    ----------
    founder : ``evpd.core.individual`` instance
        an ``Individual`` object representing the initial individual.
        The mean of the population is taken as the atomic position of this
        individual. It should ideally be an atomic configuration not too
        far from the global minimum in the PES.
        The founder must have a calculator set.

    step_size : float > 0
        initial step size used in the CMA-ES algorithm
        default 0.2 Angstrom

    covariance : None or float or 1D array or 2D array
        the initial covariance matrix. Default is the identity matrix.
        If ``covariance`` is a float, then the matrix is diagonal with that
        value on the diagonal. If it is 1D array, it is still diagonal
        with that array on the diagonal.

    dmin : float
        minimum distance between two atoms to consider an individual to
        be valid.
        Default None (0.5 of the minimum bond distance)

    random_seed : int
        random seed to be used for generating random variates.
        Default to 10
    """

    cmaes_obj = CMAES
    fitness_calc_obj = FitnessCalculator

    def __init__(self, founder, step_size=0.2, covariance=None,
                 dmin=None, random_seed=10):
        if not isinstance(founder, Individual):
            raise TypeError("The founder must be an instance of "
                            "'evpd.core.individual.Individual'")
        self.founder = founder.clone()
        if MPI.COMM_WORLD.Get_rank() == 0:
            logger.debug(f'Individual "{self.founder.my_name}" '
                         'renamed as "Founder"')
        self.founder.my_name = 'Founder'
        self.founder.dmin = dmin

        if not founder.has_proper_structure():
            raise ValueError('The Founder has an improper structure: '
                             'probably two atoms are too close together '
                             '(minimum distance between two atoms must be '
                             '> {:.3f} Angstrom). Produce a new Founder.'.format(
                                 self.founder.dmin))

        dimension = len(self.founder.positions.ravel())
        self._dimension = dimension

        if covariance is None:
            self._covariance = np.eye(dimension)
        elif isinstance(covariance, (int, float)):
            self._covariance = np.eye(dimension)*covariance
        else:
            covariance = np.array(covariance)
            if covariance.ndim == 1:
                self._covariance = np.diag(covariance)
            elif covariance.ndim == 2:
                self._covariance = covariance
            else:
                raise TypeError('The input covariance matrix must be a '
                                '2D array')

        self._population = Population(self.founder)
        self._strategyparameters = StrategyParameters(dimension)
        self._terminationcriteria = TerminationCriteria()

        self._random_seed = random_seed
        self._step_size = step_size

        self._cmaes_params = {'strategy_params': self._strategyparameters,
                              'terminator': self._terminationcriteria,
                              'mean': self.founder.positions.ravel(),
                              'step_size': self._step_size,
                              'covariance': self._covariance.copy(),
                              'random_seed': self._random_seed}

        self._external_cmaes = False    # True if the method set_cmaes is used
        self._fitness_calculator = None
        # hdf5 file which keeps track of all individuals in the population
        # along the whole evolution. The file only keeps minimal information
        self.evolution_history = 'evolution_history.hdf5'
        if MPI.COMM_WORLD.Get_rank() == 0:
            logger.debug(f'Saving population data for initialized population.')
            self.save_population(0)

    @property
    def cmaes_parameters(self):
        """ Return a dictionary with the objects needed to initialize the
        instance's CMAES object"""
        return self._cmaes_params

    @property
    def population(self):
        """ The current ``Population`` instance """
        return self._population

    @property
    def fitness_calculator(self):
        return self._fitness_calculator

    def set_strategy_parameters(self, strategy_params):
        """ Set the values of the strategy parameters to overwrite the
        default ones.

        Parameters
        ----------
        strategy_params : instance of ``StrategyParameters``
        """
        self._strategyparameters = strategy_params
        self._cmaes_params['strategy_params'] = self._strategyparameters

    def set_termination_criteria(self, termination_criteria):
        """ Set the values of the termination criteria to overwrite the
        default ones.

        Parameters
        ----------
        termination_criteria : instance of ``TerminationCriteria``
        """
        self._terminationcriteria = termination_criteria
        self._cmaes_params['terminator'] = self._terminationcriteria

    def _check_cmaes_type(self, cmaes):
        if not type(cmaes) is self.cmaes_obj:
            raise TypeError('Loaded a {} but a {} instance '
                            'is required'.format(type(cmaes),
                                                 type(self.cmaes_obj)))

    def set_cmaes(self, cmaes):
        """ Set the a custom ``CMAES`` object to overwrite the
        default one.

        Parameters
        ----------
        cmaes : instance of ``CMAES``
        """
        self._check_cmaes_type(cmaes)
        self._cmaes = cmaes
        self._cmaes_params = {'strategy_params': cmaes.StrategyParameters,
                              'terminator': cmaes.Terminator,
                              'mean': cmaes.m,
                              'covariance': cmaes.C,
                              'step_size': cmaes.step_size,
                              'random_seed': cmaes.random_seed}
        self._external_cmaes = True
        if MPI.COMM_WORLD.Get_rank() == 0:
            logger.info('An external CMAES object has been set.\n'
                        'If it is a restart, the algorithm will restart from '
                        f'generation {cmaes.g}')

    @property
    def cmaes(self):
        return self._cmaes

    def _mutate_individual(self, individual):
        x_ind = self.cmaes._mutate_single().reshape(-1, 3)
        individual.positions = x_ind

    def _generate_mutated_population(self):
        max_iter = 1000
        pop = []
        trial_no = 0
        for i in range(self.cmaes.pop_size):
            ind = self.founder.clone()
            ind.my_name = 'Individual_{}_{}'.format(self.cmaes.g + 1, i)
            self._mutate_individual(ind)
            while not ind.has_proper_structure():
                self._mutate_individual(ind)
                trial_no += 1
                if trial_no > max_iter:
                    sigma = self.cmaes.step_size
                    if isinstance(self, GpPopulationEvolver):
                        c_a = self.cmaes.gradient_coefficient
                    else:
                        c_a = 0
                    raise RuntimeError(
                        'Mutation cannot generate a valid '
                        'structure after {} trials. '
                        'You are probably using a too large step_size '
                        '(current value = {:.3f}) or a too large '
                        'gradient coefficient (current value = {:.3f})'
                        .format(max_iter, sigma, c_a))
            pop.append(ind)
        return Population(pop)

    def get_object_parameters(self):
        """ Returns the object parameters as a NumPy 2D array of shape
        (N, d), where N is the number of individuals in the population and
        d is the search space dimension
        """
        pop = self.population
        size = (self.cmaes.pop_size, self._dimension)
        x = np.empty(size) 
        for i, ind in enumerate(pop):
            x[i] = ind.positions.flatten()
        return x

    def _get_fitness_calculator(self):
        return self.fitness_calc_obj(self.population)

    def _set_up_cmaes(self):
        if not self._external_cmaes:
            self._cmaes = self.cmaes_obj(**self._cmaes_params)

    def _evolve(self):
        if MPI.COMM_WORLD.Get_rank() == 0:
            logger.debug(f'Mutating individuals for generation '
                         f'{self.cmaes.g + 1}')
        pop = self._generate_mutated_population()
        self._population = pop
        self._fitness_calculator.population = self.population
        self.cmaes.set_fitness_calculator(self.fitness_calculator)
        self.cmaes.set_mutated_offspring(self.get_object_parameters())
        if MPI.COMM_WORLD.Get_rank() == 0:
            logger.debug('Mutation completed.')

    def _initialize_evolution(self):
        if MPI.COMM_WORLD.Get_rank() == 0:
            logger.debug('Initializing evolution: setting up the CMAES')
        self._set_up_cmaes()
        self._fitness_calculator = self._get_fitness_calculator()
        self._evolve()

    def evolve_population(self):
        """ Evolve the current population.
        Returns a generator with the relevant parameters of the
        current generation.
        """
        if MPI.COMM_WORLD.Get_rank() == 0:
            logger.info('Initializing the evolution process')
        self._initialize_evolution()
        if MPI.COMM_WORLD.Get_rank() == 0:
            logger.info('Initialization completed, commence the evolution')
        for params in self.cmaes.evolve(manual_mutation=True):
            if MPI.COMM_WORLD.Get_rank() == 0:
                g = params['g']
                logger.info(f'COMPLETED CALCULATIONS FOR GENERATION {g}.')
                logger.debug(f'Saving population data for generation {g}.')
                self.save_population(g)
            yield params
            if MPI.COMM_WORLD.Get_rank() == 0:
                logger.debug('Initializing next generation.')
            self._evolve()

    def save_population(self, generation):
        """ Append the current population to ``self.evolution_history``
        file

        Parameters
        ----------
        generation : int
            the index of the current generation. Used to create a
            corresponding new group in the hdf5 file
        """
        # to be consistent with the ids created by the function in evpd.misc
        df = '<f8'
        di = '<u1'
        no_dec = 10
        comp_kwargs = {'compression': 'gzip', 'compression_opts': 9}
        if not os.path.isfile(self.evolution_history):
            logger.debug('Creating new history file '
                         f'{self.evolution_history}')
            cell = self.founder.cell[:].copy()
            cell = np.array(cell, dtype=df).round(no_dec)
            numbers = self.founder.numbers.copy()
            numbers = np.array(numbers, dtype=di)
            pbc = self.founder.pbc.copy()
            pbc = np.array(pbc, dtype=di)

            with h5py.File(self.evolution_history, 'w') as f:
                group = f.create_group('system')
                group.create_dataset('cell', data=cell, shape=(3, 3),
                                     dtype=df, **comp_kwargs)
                group.create_dataset('atomic_numbers', data=numbers,
                                     shape=(len(numbers), ), dtype=di,
                                     **comp_kwargs)
                group.create_dataset('pbc', data=pbc, shape=(3, ),
                                     dtype=df, **comp_kwargs)

        d = self.population[0].positions.ravel().shape[0]
        shape = (len(self.population), d)
        names = [x.my_name for x in self.population]
        names = np.array(names, dtype='<S30')
        positions = []
        for ind in self.population:
            pos = ind.positions.ravel().astype(df).round(no_dec)
            positions.append(pos)
        positions = np.vstack(positions)
        logger.debug(f'Adding {positions.shape[0]} new instances of '
                     f'generation {generation} to history '
                     f'file {self.evolution_history}.')
        with h5py.File(self.evolution_history, 'a') as f:
            try:
                group = f.create_group('Generation_' + str(generation))
                group.create_dataset('labels', data=names,
                                     shape=(len(names), ),
                                     dtype='<S30', **comp_kwargs)
                group.create_dataset('positions', data=positions, shape=shape,
                                     dtype=df, **comp_kwargs)
            except ValueError:  # Unable to create group (name already exists)
                logger.debug(f'Population data for generation {generation} '
                             'are already present in the dataset.')


class SSPopulationEvolver(PopulationEvolver):
    """ Add to the initial covariance matrix a rank-s matrix increasing the
    variance for coordinates representing atoms close to the point defect
    position

    Parameters
    ----------
    nn_cutoff : float
        cutoff radius, in Angstrom, including the atoms used to build the
        rank-s matrix

    c_r : float
        coefficient to control the contribution of the rank-s matrix to
        the initial covariance matrix

    founder : evpd.core.individual instance
        an ``Individual`` object representing the initial individual.
        The mean of the population is taken as the atomic position of this
        individual. It should ideally be an atomic configuration not too
        far from the global minimum in the PES.
        The founder must have a calculator set.

    kwargs : other keyword arguments necessary to initialize a ``PopulationEvolver``
        instance
    """
    def __init__(self, nn_cutoff, c_r, founder, **kwargs):
        super().__init__(founder, **kwargs)
        self._nn_cutoff = nn_cutoff
        self._cr = c_r

    @property
    def number_of_nn(self):
        """ The number of nearest neighbors atoms within ``self.nn_cutoff``
        """
        if not hasattr(self, '_number_nn'):
            self._find_subspace_basis()
        return self._number_nn

    @property
    def nn_cutoff(self):
        """ Cutoff selecting the NN to the defect which will form the basis
        for the selected subspace
        """
        return self._nn_cutoff

    @property
    def basis_coefficients(self):
        """ The distances of the atoms within the cutoff and the coefficients
        per atom which are used to add the rank-s matrix
        to the initial covariance matrix
        """
        return (self._sorted_distances_within.copy(),
                self._basis_coefficients[::3].copy())

    @property
    def selected_subspace_basis(self):
        """ The basis spanning the selected subspace. Order with respect to
        the atomic distances from the defect
        """
        if not hasattr(self, '_number_nn'):
            self._find_subspace_basis()
        return self._subspace_basis.copy()

    @property
    def atoms_within_cutoff(self):
        """ Indices of the atoms within the cutoff """
        if not hasattr(self, '_number_nn'):
            self._find_subspace_basis()
        return self._atoms_within_cutoff

    def _find_subspace_basis(self):
        """ Find the atoms within ``self.number_of_nn`` from
        the defect and use their coordinates (plus those of the defect,
        if it is an atom) to generate the selected-subspace basis
        """
        cutoff = self.nn_cutoff
        founder = self.founder
        d_from_def = founder.distances_from_defect
        def_pos = founder.defect_position
        indices = np.argsort(d_from_def)
        sorted_distances = d_from_def[indices]
        self._Rmax = sorted_distances[-1]
        within_cf = sorted_distances <= cutoff
        within_atoms = indices[within_cf]
        self._Rc = sorted_distances[len(within_atoms) - 1]
        if self._Rc > self._Rmax:    # e.g. if the user chooses a cutoff larger
            self._Rc = self._Rmax    # than the supercell
        self._sorted_distances_within = sorted_distances[within_cf]
        has_def = (np.abs(founder.get_scaled_positions() - def_pos) < 1e-3)
        has_def = has_def.all(axis=1).any()
        if has_def:
            self._number_nn = len(np.unique(sorted_distances[within_cf])) - 1
            self._dnn = sorted_distances[1]
        else:
            self._number_nn = len(np.unique(sorted_distances[within_cf]))
            self._dnn = sorted_distances[0]
        self._atoms_within_cutoff = within_atoms
        m = len(self._atoms_within_cutoff)
        # basis vectors as row vectors
        basis = np.zeros((3*m, self._dimension))
        for i, atom in enumerate(self._atoms_within_cutoff):
            basis[3*i:3*i + 3, 3*atom:3*atom + 3] = np.eye(3)
        self._subspace_basis = basis

    def _calculate_basis_coefficients(self):
        d = self._sorted_distances_within
        betas = 1/((1 + d)**2)
        weights = np.repeat(betas, 3)
        self._basis_coefficients = weights*weights

    def _calculate_rank_s_matrix(self):
        #omag = np.mean(np.diag(self._covariance))    # magnitude of cov
        omag = 1
        basis = self.selected_subspace_basis.T
        self._calculate_basis_coefficients()
        basis *= np.sqrt(self._basis_coefficients)
        matrix = np.dot(basis, basis.T)*omag
        return matrix

    def _set_up_cmaes(self):
        if not self._external_cmaes:
            matrix = self._calculate_rank_s_matrix()*np.square(self._cr)
            C_0 = self._covariance
            self._cmaes_params['covariance'] = C_0 + matrix
        super()._set_up_cmaes()


class GpPopulationEvolver(SSPopulationEvolver):
    """ Exploit the gradient during the run.

    Parameters
    ----------
    c_alpha : float
        coefficient describing the relevance of the gradient term

    nn_cutoff : float
        cutoff radius, in Angstrom, including the atoms used to build the
        rank-s matrix

    c_r : float
        coefficient to control the contribution of the rank-s matrix to
        the initial covariance matrix

    founder : evpd.core.individual instance
        an ``Individual`` object representing the initial individual.
        The mean of the population is taken as the atomic position of this
        individual. It should ideally be an atomic configuration not too
        far from the global minimum in the PES.
        The founder must have a calculator set.

    kwargs : other keyword arguments necessary to initialize a ``PopulationEvolver``
        instance
    """

    cmaes_obj = GpCMAES
    fitness_calc_obj = FitnessGradientCalculator

    def __init__(self, c_alpha, nn_cutoff, c_r, founder, **kwargs):
        super().__init__(nn_cutoff, c_r, founder, **kwargs)
        self._c_alpha = c_alpha

    @property
    def gradient_coefficient(self):
        return self._c_alpha

    def _set_up_cmaes(self):
        if not self._external_cmaes:
            matrix = self._calculate_rank_s_matrix() * np.square(self._cr)
            C_0 = self._covariance
            self._cmaes_params['covariance'] = C_0 + matrix
            self._cmaes = self.cmaes_obj(**self._cmaes_params)
            self.cmaes.set_gradient_coefficient(self._c_alpha)
        else:
            self._c_alpha = self.cmaes.gradient_coefficient


class RSPopulationEvolver(SSPopulationEvolver):
    """ Restricted-subspace population evolver: only the genotype for
    atoms inside a cutoff radius is considered

    Parameters
    ----------
    nn_cutoff : float
        cutoff radius, in Angstrom, including the atoms used to build the
        rank-s matrix

    c_r : float
        coefficient to control the contribution of the rank-s matrix to
        the initial covariance matrix

    founder : evpd.core.individual instance
        an ``Individual`` object representing the initial individual.
        The mean of the population is taken as the atomic position of this
        individual. It should ideally be an atomic configuration not too
        far from the global minimum in the PES.
        The founder must have a calculator set.

    kwargs : other keyword arguments necessary to initialize a ``PopulationEvolver``
        instance


    Notes
    -----
    Similar to ``SSPopulationEvolver`` but only the atoms within the cutoff
    are moved.
    """

    fitness_calc_obj = RSFitnessCalculator

    @property
    def use_reduced_population_size(self):
        """ Bool, if True, choose automatically the population size
        as based on the dimension of the restricted subspace. If False,
        uses the population size given by the ``StrategyParameters``
        instance given at initialization. Default False.
        """
        return self._use_reduced_pop_size

    @use_reduced_population_size.setter
    def use_reduced_population_size(self, value):
        self._use_reduced_pop_size = value

    def get_object_parameters(self):
        """ Returns the object parameters as a NumPy 2D array of shape
        (N, d), where N is the number of individuals in the population and
        d is the dimension of the restricted subspace
        """
        x_large = super().get_object_parameters()
        size = len(self.founder.positions.flatten())
        x_large.reshape((-1, size))
        indices = self.atoms_within_cutoff
        size = (self.cmaes.pop_size, self.cmaes.dimension)
        x = np.empty(size)
        for j, index in enumerate(indices):
            x[:, 3*j:3*j+3] = x_large[:, 3*index:3*index + 3]
        return x

    def _mutate_individual(self, individual):
        indices = self.atoms_within_cutoff
        ext_x_ind = individual.positions.flatten()
        x_ind = self.cmaes._mutate_single()
        for j, index in enumerate(indices):
            ext_x_ind[3 * index:3 * index + 3] = x_ind[3 * j:3 * j + 3]
        individual.positions = ext_x_ind.reshape(-1, 3)

    def _prepare_distribution_parameters(self, indices):
        dim = len(indices)*3
        mean = self.founder.positions.ravel()
        matrix = self._calculate_rank_s_matrix()*np.square(self._cr)
        C_0 = self._covariance
        C_0_r = np.zeros((dim, dim))
        matrix = np.diag(matrix)
        d_matrix = np.zeros(dim)
        d_mean = np.zeros(dim)
        for i, ind in enumerate(indices):
            d_matrix[3*i:3*i + 3] = matrix[3*ind:3*ind + 3]
            d_mean[3*i:3*i + 3] = mean[3*ind:3*ind + 3]
            for j, indj in enumerate(indices):
                C_0_r[3*i:3*i + 3, 3*j:3*j + 3] = C_0[3*ind:3*ind + 3,
                                                      3*indj:3*indj + 3]
        matrix = np.diag(d_matrix)
        self._cmaes_params['mean'] = d_mean
        self._cmaes_params['covariance'] = C_0_r + matrix

    def _get_fitness_calculator(self):
        return self.fitness_calc_obj(
            self.population, self.atoms_within_cutoff)

    def _prepare_strategy_parameters(self, indices):
        dim = len(indices)*3
        sp = self._strategyparameters
        pop_size = sp.pop_size
        weights = sp.weights
        c_sigma = sp.c_sigma
        d_sigma = sp.d_sigma
        c_c = sp.c_c
        c_1 = sp.c_1
        c_mu = sp.c_mu
        alpha_cov = sp.alpha_cov
        std_min = sp.std_min
        c_g = sp.c_g
        if hasattr(self, '_use_reduced_pop_size'):
            if self.use_reduced_population_size is True:
                pop_size = None
                weights = None
                c_sigma = None
                d_sigma = None
                c_c = None
                c_mu = None
        strategy_params = StrategyParameters(
            dim, pop_size=pop_size,
            weights=weights, c_sigma=c_sigma, d_sigma=d_sigma,
            c_c=c_c, c_1=c_1, c_mu=c_mu, alpha_cov=alpha_cov,
            std_min=std_min, c_g=c_g)
        self.set_strategy_parameters(strategy_params)

    def _set_up_cmaes(self):
        if not self._external_cmaes:
            indices = self.atoms_within_cutoff
            self._prepare_distribution_parameters(indices)
            self._prepare_strategy_parameters(indices)
            self._cmaes = self.cmaes_obj(**self._cmaes_params)


class RSPopulationEvolverGrad(RSPopulationEvolver, GpPopulationEvolver):
    """
    Parameters
    ----------
    c_alpha : float
        coefficient describing the relevance of the gradient term

    nn_cutoff : float
        cutoff radius, in Angstrom, including the atoms used to build the
        rank-s matrix

    c_r : float
        coefficient to control the contribution of the rank-s matrix to
        the initial covariance matrix

    founder : evpd.core.individual instance
        an ``Individual`` object representing the initial individual.
        The mean of the population is taken as the atomic position of this
        individual. It should ideally be an atomic configuration not too
        far from the global minimum in the PES.
        The founder must have a calculator set.

    kwargs : other keyword arguments necessary to initialize a ``PopulationEvolver``
        instance


    Notes
    -----
    Similar to ``RSPopulationEvolver`` but gradients are also used.
    are moved.
    """

    cmaes_obj = GpCMAES
    fitness_calc_obj = RSFitnessGradientCalculator

    def __init__(self, c_alpha, nn_cutoff, c_r, founder, **kwargs):
        GpPopulationEvolver.__init__(self, c_alpha=c_alpha,
                                     nn_cutoff=nn_cutoff, c_r=c_r,
                                     founder=founder, **kwargs)

    def _set_up_cmaes(self):
        if not self._external_cmaes:
            indices = self.atoms_within_cutoff
            self._prepare_distribution_parameters(indices)
            self._prepare_strategy_parameters(indices)
            self._cmaes = self.cmaes_obj(**self._cmaes_params)
            self.cmaes.set_gradient_coefficient(self._c_alpha)
        else:
            self._c_alpha = self.cmaes.gradient_coefficient


class RSPopulationEvolverMetamodel(RSPopulationEvolver):
    """ RS Fitness Calculator with a metamodel to be trained on-the-fly

    Parameters
    ----------
    metamodel : a ``Metamodel`` object that will be used to make the energy
        predictions

    dataset : string
        the name of the .hdf5 file which will be used to write/read the
        training data

    nn_cutoff : float
        cutoff radius, in Angstrom, including the atoms used to build the
        rank-s matrix

    c_r : float
        coefficient to control the contribution of the rank-s matrix to
        the initial covariance matrix

    founder : evpd.core.individual instance
        an ``Individual`` object representing the initial individual.
        The mean of the population is taken as the atomic position of this
        individual. It should ideally be an atomic configuration not too
        far from the global minimum in the PES.
        The founder must have a calculator set.

    min_generation : int. Default 0
        use the meta-model only in the current generation is
        larger or equal than ``min_generation``

    train_kwargs : dict
        the keyword-argument values used to train the metamodel

    kwargs : other keyword arguments necessary to initialize a ``PopulationEvolver``
        instance
    """

    fitness_calc_obj = MetaRSFitnessCalculator

    def __init__(self, metamodel, dataset, nn_cutoff, c_r, founder,
                 min_generation=0, train_kwargs=dict(), **kwargs):
        super().__init__(nn_cutoff=nn_cutoff, c_r=c_r,
                         founder=founder, **kwargs)
        self.metamodel = metamodel
        self.dataset = dataset
        self.min_generation = min_generation
        self.train_kwargs = train_kwargs

    def _get_fitness_calculator(self):
        return self.fitness_calc_obj(self.population,
                                     self.atoms_within_cutoff,
                                     self.metamodel,
                                     self.dataset,
                                     min_generation=self.min_generation,
                                     train_kwargs=self.train_kwargs)


class AnalizeRun:
    """ Helper class for analyzing the evolution of the population

    Parameters
    ----------
    Evolver : ``PopulationEvolver`` derived instance
        the evolver to be analyzed.
        If Evolver is set to None, then the class
        can be used to analyze an already existing
        simulation dataframe (set with the method 
        ``load_dataframe``.
    """
    columns = ['generation', 'seed', 'defect_pos',
               'c_alpha (A^2/eV)', 'nn_dist (A)', 'c_r',
               'step_size', 'mean E (eV)', 'std E (eV)',
               'max E (eV)', 'min E (eV)',
               'grad (eV/A)', 'ffe']

    def __init__(self, evolver):
        if evolver:
            if not isinstance(evolver, PopulationEvolver):
                raise TypeError('Evolver must be a PopulationEvolver '
                                '(sub)instance')
            self._evolver = evolver
            self._ffe = 0
            self._data = []

    @property
    def evolver(self):
        return self._evolver

    def initialize(self):
        """ Initialize the evolution

        Returns
        -------
        dataframe : pandas DataFrame with the elements for
            generation 0
        """
        if MPI.COMM_WORLD.Get_rank() == 0:
            logger.debug('Initializing the Run')
        try:  # if starting from a previous run
            generation = self.evolver.cmaes.g - 1
        except AttributeError:
            generation = 0
        defect_pos = str(self.evolver.founder.defect_position)
        self._defect_pos = defect_pos
        if isinstance(self.evolver, GpPopulationEvolver):
            c_alpha = self.evolver.gradient_coefficient
        else:
            c_alpha = 0
        self._c_alpha = c_alpha
        if isinstance(self.evolver, SSPopulationEvolver):
            nn_dist = self.evolver._nn_cutoff
            c_r = self.evolver._cr
        else:
            nn_dist = np.nan
            c_r = 0
        self._nn_dist = nn_dist
        self._c_r = c_r
        sigma = self.evolver._step_size
        energy = self.evolver.founder.cost
        self._ffe += self.evolver.founder.total_energy_calculations
        ffe = self._ffe
        if isinstance(self.evolver, GpPopulationEvolver):
            grad = self.evolver.founder.calc.get_forces().ravel()
            grad = np.linalg.norm(grad)
        else:
            grad = np.nan

        row = {'generation': generation,
               'seed': self.evolver._random_seed,
               'defect_pos': defect_pos, 'c_alpha (A^2/eV)': c_alpha,
               'nn_dist (A)': nn_dist, 'c_r': c_r, 'step_size': sigma,
               'mean E (eV)': energy, 'std E (eV)': 0,
               'max E (eV)': energy, 'min E (eV)': energy,
               'grad (eV/A)': grad, 'ffe': ffe}
        self._data.append(row)
        return pd.DataFrame(self._data, columns=self.columns)

    def evolve(self):
        """ Evolve generation-by-generation

        Yields
        ------
        dataframe : pandas DataFrame updated to the
            current generation
        """
        for params in self.evolver.evolve_population():
            energies = -params['fitnesses']
            generation = params['g']
            C = params['C']
            index = np.argsort(-energies)
            emin = np.min(energies)
            emax = np.max(energies)
            emean = np.mean(energies)
            estd = np.std(energies)
            ffe = self._ffe
            for ind in self.evolver.population:
                ffe += ind.total_energy_calculations
            self._ffe = ffe
            if isinstance(self.evolver, GpPopulationEvolver):
                grad = self.evolver.cmaes.gradients
                grad = np.linalg.norm(np.mean(grad, axis=0))
                c_alpha = self.evolver.cmaes.gradient_coefficient
            else:
                grad = np.nan
                c_alpha = 0
            sigma = params['step_size']
            row = {'generation': generation,
                   'seed': self.evolver.cmaes.random_seed,
                   'defect_pos': self._defect_pos,
                   'c_alpha (A^2/eV)': c_alpha,
                   'nn_dist (A)': self._nn_dist, 'c_r': self._c_r,
                   'step_size': sigma, 'mean E (eV)': emean,
                   'std E (eV)': estd,
                   'max E (eV)': emax, 'min E (eV)': emin,
                   'grad (eV/A)': grad, 'ffe': ffe}

            self._data.append(row)
            dataframe = pd.DataFrame(self._data, columns=self.columns)
            self.dataframe = dataframe.copy()
            yield dataframe

    def run(self):
        """ Evolve the population until a termination criterion is met.

        Returns
        -------
        dataframe : pandas DataFrame
            stores information about the evolution of ``Evolver``
        """
        data_init = self.initialize()
        yield data_init
        for dataframe in self.evolve():
            yield dataframe

    @staticmethod
    def plot_data_vs_generation(df, keys, other_keys=None, samples=[1],
                                serrors=[0], alpha=0.05, **kwargs):
        """ Plot the evolution of ``key`` and eventually ``other_keys``,
        in ``df`` with respect
        to the generation number.

        Parameters
        ----------
        df : pandas data frame
            it must contains at least 2 columns:
            'generation', with the generation number,
            and ``key``.

        keys : list of strings
            the column labels in ``df`` to be plotted.
            If this is an averaged value, the sample stds
            are given by ``se``

        other_keys : None or list of strings
            the eventual other column labels to be plotted

        samples : list of int
            if one of ``keys`` is an average, it is its sample size.

        serrors : list of float
            if one of ``keys`` is an average, it is its sample std.
            This will be used to calculate the confidence intervals

        alpha : float in (0, 1)
            defines the wished (1-alpha)*100% confidence interval

        kwargs : dictionary
            keyword-value pairs for tuning the plot parameters
            see documentation of ``pandas.DataFrame.plot.line``
        """
        figsize = kwargs.get('figsize', (10, 8))
        use_index = False
        fontsize = kwargs.get('fontsize', 24)
        linewidth = kwargs.get('linewidth', 2)
        x = df['generation'].values
        cfs = []
        cfas = []
        cfbs = []
        for i, key in enumerate(keys):
            s = samples[i]
            se = serrors[i]
            cf = scipy.stats.t.ppf((2-alpha)/2, s-1)
            cfa = df[key] - cf*se/np.sqrt(s)
            cfb = df[key] + cf*se/np.sqrt(s)
            cfs.append(cf)
            cfas.append(cfa)
            cfbs.append(cfb)
        if len(keys) == 1:
            ax = df.plot.line('generation', keys, figsize=figsize,
                              use_index=use_index, fontsize=fontsize,
                              linewidth=linewidth,
                              color='black')
        else:
            ax = df.plot.line('generation', keys, figsize=figsize,
                              use_index=use_index, fontsize=fontsize,
                              linewidth=linewidth)
        ax.plot(x, df[other_keys].values, linestyle='--', color='blue')
        for i, (cfa, cfb) in enumerate(zip(cfas, cfbs)):
            ax.plot(x, cfa.values, color='red', linestyle='--', linewidth=2)
            ax.plot(x, cfb.values, color='red', linestyle='--', linewidth=2)
            if i == 0:
                ax.fill_between(x, cfa.values, cfb.values, alpha=0.5, color='red',
                                label='{:d}% C.I.'.format(int((1 - alpha)*100)))
            else:
                ax.fill_between(x, cfa.values, cfb.values, alpha=0.5, color='red')
        plt.legend(loc=1, prop={'size': 18})
        return ax

    def plot_energy_vs_generation(self, **kwargs):
        """ Plots the evolution of the mean population energy
        as a function of the generation.

        Parameters
        ----------
        kwargs : dictionary
            keyword-value pairs for tuning the plot parameters
            see documentation of ``pandas.DataFrame.plot.line``
        """
        df = self.dataframe
        keys = ['max E (eV)', 'min E (eV)']
        s = self.evolver.cmaes.pop_size
        se = df['std E (eV)']*np.sqrt(s/(s-1))
        AnalizeRun.plot_data_vs_generation(df, ['mean E (eV)'], keys,
                                           samples=[s], serrors=[se],
                                           **kwargs)
        plt.show()

    def load_dataframe(self, df):
        """ Use this method to analyze a proper simulation dataframe
        without need of running the whole evolutionary process

        Parameters
        ----------
        df : pandas DataFrame
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError('The dataframe should be a pandas one')
        if not set(self.columns).issubset(set(df.columns)):
            raise ValueError('The dataframe should possess at least '
                             'these columns: {}'.format(self.columns))
        self.dataframe = df.copy()
