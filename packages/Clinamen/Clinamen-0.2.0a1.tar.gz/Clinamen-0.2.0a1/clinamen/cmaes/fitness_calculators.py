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
import h5py
from mpi4py import MPI

from ase import Atoms

from clinamen.evpd import ROOT_LOGGER as logger
from clinamen.evpd.core.population import Population
from clinamen.evpd.core.individual import Individual
from clinamen import INDIVIDUALS_FLOAT_DTYPE as DTYPE


proc_rank = MPI.COMM_WORLD.Get_rank()


def write_train_hdf5(file_name, population, energies, forces, name=None):
    """ Append new data to an existing dataset, if the dataset
    does not exist, create a new one

    Parameters
    ----------
    file_name : string
        the dataset name

    population : `Population` instance
        the new individuals to be added to the dataset

    energies : array-like of shape (n_individuals, )
        the energies of the individuals in ``population``

    forces : 2D array-like of shape (n_individuals, 3*no_atoms)
        the forces of the individuals in ``population``

    name : string. Default None
        the system name. A tag that specifies the system when the
        dataset is created. If the dataset already exists, it checks
        the it corresponds to system ``name``
    """
    comp_kwargs = {'compression': 'gzip', 'compression_opts': 9}
    founder = population[0]
    d = population[0].positions.ravel().shape[0]
    shape_x = (None, d)
    shape_y = (None, )
    shape_dy = (None, d)
    xs = [x.positions.ravel() for x in population]
    X = np.vstack(xs)
    y = np.array(energies)
    dy = np.array(forces)
    y = np.atleast_1d(y)
    X, dy = np.atleast_2d(X, dy)
    new_dataset = True
    if os.path.isfile(file_name):
        new_dataset = False
        # get data to check dataset consistency
        if proc_rank == 0:
            logger.debug('Found an existing dataset with '
                         f'training data: {file_name}')
        with h5py.File(file_name, 'r') as f:
            sys_name = f['system'].attrs['name'].decode()
            atomic_numbers = np.array(f['system']['atomic_numbers'])
            cell = np.array(f['system']['cell'])
            pbc = np.array(f['system']['pbc'])
        if name is not None:
            c0 = (name == sys_name)
        else:
            c0 = True
        for individual in population:
            c1 = np.allclose(atomic_numbers, individual.get_atomic_numbers(),
                             rtol=0, atol=1e-9)
            c2 = np.allclose(cell, individual.get_cell()[:],
                             rtol=0, atol=1e-9)
            c3 = np.allclose(pbc, individual.get_pbc(),
                             rtol=0, atol=1e-9)
            if not np.all([c0, c1, c2, c3]):
                indices = np.where(np.array([c0, c1, c2, c3]) == False)
                error_msg = (f'Individual {individual.my_name} '
                              'does not conform with the dataset '
                             f'{file_name}: ')
                for ind in indices:
                    if ind == 0:
                        ind_msg = f'System name "{name}" is not "{sys_name}". '
                    elif ind == 1:
                        ind_msg = 'Atomic numbers do not agree with those in the dataset. '
                    elif ind == 2:
                        ind_msg = 'Unit cell does not agree with that of the dataset. '
                    elif ind == 3:
                        ind_msg = 'PBC do not agree with those of the dataset. '
                    error_msg += ind_msg
                raise ValueError(error_msg)
    if new_dataset:
        if proc_rank == 0:
            logger.debug('A new dataset with training data will be created '
                         f'with name {file_name}')
            with h5py.File(file_name, 'w') as f:
                system = f.create_group('system')
                if name is None:
                    sys_name = 'system'
                else:
                    sys_name = name
                system.attrs['name'] = np.string_(sys_name)
                atomic_numbers = founder.get_atomic_numbers()
                system.create_dataset('atomic_numbers', data=atomic_numbers,
                                      dtype=np.uint8, **comp_kwargs)
                cell = founder.get_cell()[:]
                system.create_dataset('cell', data=cell, shape=(3, 3),
                                      dtype=DTYPE, **comp_kwargs)
                pbc = founder.get_pbc()
                system.create_dataset('pbc', data=pbc, dtype=bool,
                                      **comp_kwargs)
                data = f.create_group('data')
                data.create_dataset('X', data=X, dtype=DTYPE,
                                    maxshape=shape_x, **comp_kwargs)
                data.create_dataset('y', data=y, dtype=DTYPE,
                                    maxshape=shape_y, **comp_kwargs)
                data.create_dataset('dy', data=dy, dtype=DTYPE,
                                    maxshape=shape_dy, **comp_kwargs)
                logger.debug(f'Added {X.shape} positions, '
                             f'{y.shape} energies and {dy.shape} forces '
                             f'to training set {file_name}')
    else:
        with h5py.File(file_name, 'a') as f:
            dset_X = f['data']['X']
            dset_y = f['data']['y']
            dset_dy = f['data']['dy']
            if proc_rank == 0:
                logger.debug(f'Found {dset_X.shape} positions, '
                             f'{dset_y.shape} energies and {dset_dy.shape} '
                             f'forces in training set {file_name}')
            dset_X.resize(dset_X.shape[0] + X.shape[0], axis=0)
            dset_X[-X.shape[0]:] = X
            dset_y.resize(dset_y.shape[0] + y.shape[0], axis=0)
            dset_y[-y.shape[0]:] = y
            dset_dy.resize(dset_dy.shape[0] + dy.shape[0], axis=0)
            dset_dy[-dy.shape[0]:] = dy
            if proc_rank == 0:
                logger.debug('New data have been appended. There are now: '
                             f'{dset_X.shape} positions, '
                             f'{dset_y.shape} energies and {dset_dy.shape} '
                             f'forces in training set {file_name}')


def read_train_hdf5(file_name):
    proc_rank = MPI.COMM_WORLD.Get_rank()
    with h5py.File(file_name, 'r') as f:
        name = f['system'].attrs['name'].decode()
        atomic_numbers = np.array(f['system']['atomic_numbers'])
        cell = np.array(f['system']['cell'])
        pbc = np.array(f['system']['pbc'])
        data = f['data']
        # Cartesian positions
        X_data = np.array(data['X'])
        # energies
        y_data = np.array(data['y'])
        # forces
        dy_data = np.array(data['dy'])
        X_size = X_data.shape[0]
        if not(X_size == y_data.shape[0] and X_size == dy_data.shape[0]):
            raise ValueError('Dataset is probably corrupt: '
                             f'got {X_size} instances for positions, '
                             f'{y_data.shape[0]} for energies and '
                             f'{dy_data.shape[0]} for forces')
        if proc_rank == 0:
            logger.debug(f'Training dataset {file_name} has been read. '
                         f'Found {X_data.shape} positions, '
                         f'{y_data.shape} energies and {dy_data.shape} '
                         f'forces.')

        return X_data, y_data, dy_data, name, atomic_numbers, cell, pbc


class FitnessCalculator:
    """ Fitness calculator for Population objects

    Parameters
    ----------
    population : Population instance
        the current individual population
    """
    comm = MPI.COMM_WORLD
    comm_size = comm.Get_size()
    proc_rank = comm.Get_rank()

    def __init__(self, population):
        if not isinstance(population, Population):
            raise TypeError("The population must be an instance of "
                            "'evpd.core.population.Population'")
        self._population = population
        self.fitnesses = None
        self.N = len(self.population)
        self.d = len(self.population[0].positions.ravel())

    @property
    def population(self):
        return self._population

    @population.setter
    def population(self, value):
        if not isinstance(value, Population):
            raise TypeError("The population must be an instance of "
                            "'evpd.core.population.Population'")
        self._population = value
        self.N = len(self.population)

    def _check_input_shape(self, input_, shape):
        if not input_.shape == shape:
            raise ValueError("The input has shape {}; expected shape "
                             "{}".format(input_.shape, shape))

    def _update_population_positions(self):
        for i, ind in enumerate(self.population):
            ind.positions = self.x[i].reshape((-1, 3))

    def set_object_parameters(self, x):
        """ Set the object parameters to the individuals in ``self.population``

        Parameters
        ----------
        x : 2D NumPy array
            shape (N, d), with N is the number of individuals in the
            population and d is the dimensionality of the search space
        """
        shape = (self.N, self.d)
        self._check_input_shape(x, shape)
        self.x = x.copy()
        self._update_population_positions()

    def _get_indices_to_process(self, size=None):
        if size is None:
            size = len(self.population)
        batches_size = size//self.comm_size
        batches_rem = size % self.comm_size
        if self.proc_rank < batches_rem:
            ind_start = self.proc_rank*(batches_size + 1)
            ind_end = ind_start + batches_size
        else:
            ind_start = self.proc_rank*batches_size + batches_rem
            ind_end = ind_start + batches_size - 1
        return ind_start, ind_end

    def _gather_fitnesses(self, my_fitnesses):
        fitnesses = []
        if self.proc_rank == 0:
            fitnesses.extend(my_fitnesses)
            for j in range(1, self.comm_size):
                logger.debug(f'Process {self.proc_rank} is receiving the '
                             'fitnesses from slaves with tag 1')
                logger.debug(f'Process {j} is sending its '
                             'fitness to master with tag 1')
                other_fitnesses = self.comm.recv(source=j, tag=1)
                logger.debug(f'Fitness received from processor {j}')
                fitnesses.extend(other_fitnesses)
        else:
            self.comm.send(my_fitnesses, dest=0, tag=1)
        # update also all other processes
        if self.proc_rank == 0:
            logger.debug(f'Starting sync for processes')
        fitnesses = self.comm.bcast(fitnesses, root=0)
        self.comm.Barrier()
        return fitnesses

    def get_fitness(self):
        # update individuals
        start, end = self._get_indices_to_process()
        if self.proc_rank == 0:
            logger.debug(f'The FitnessCalculator in process {self.proc_rank} '
                         f'of {self.comm_size} will calculate the fitness '
                         f'of individuals from {start} to {end}')
            for j in range(1, self.comm_size):
                r_start = self.comm.recv(source=j, tag=32)
                r_end = self.comm.recv(source=j, tag=33)
                logger.debug(f'The FitnessCalculator in process {j} '
                             f'of {self.comm_size} will calculate the fitness '
                             f'of individuals from {r_start} to {r_end}')
        else:
            self.comm.send(start, dest=0, tag=32)
            self.comm.send(end, dest=0, tag=33)
        local_pop = self.population[start:end + 1]
        my_fitnesses = local_pop.individuals_fitness
        self.comm.Barrier()
        fitnesses = self._gather_fitnesses(my_fitnesses)
        self.fitnesses = np.array(fitnesses)
        return np.array(fitnesses)


class FitnessGradientCalculator(FitnessCalculator):
    def _gather_gradients(self, my_grads, start, end):
        grads = np.empty((self.N, self.d), dtype=DTYPE)
        if self.proc_rank != 0:
            data = (start, end)
            self.comm.send(data, dest=0, tag=2)
        if self.proc_rank == 0:
            grads[start:end + 1] = my_grads
            for j in range(1, self.comm_size):
                ostart, oend = self.comm.recv(source=j, tag=2)
                other_grads = np.empty((oend + 1 - ostart, self.d),
                                       dtype=DTYPE)
                self.comm.Recv(other_grads, source=j, tag=3)
                grads[ostart:oend + 1] = other_grads
        else:
            self.comm.Send(my_grads, dest=0, tag=3)
        # update all other processes
        self.comm.Bcast(grads, root=0)
        self.comm.Barrier()
        return grads

    def get_gradients(self):
        """ From a ``Population`` instance with individuals
        with an attached calculator, that RETURNS FORCES, computes
        and returns the gradients for individuals in the population.
        """
        start, end = self._get_indices_to_process()
        if self.proc_rank == 0:
            logger.debug(f'The FitnessCalculator in process {self.proc_rank} '
                         f'of {self.comm_size} will calculate the gradients '
                         f'of individuals from {start} to {end}')
            for j in range(1, self.comm_size):
                r_start = self.comm.recv(source=j, tag=32)
                r_end = self.comm.recv(source=j, tag=33)
                r_rank = self.comm.recv(source=j, tag=34)
                logger.debug(f'The FitnessCalculator in process {r_rank} '
                             f'of {self.comm_size} will calculate the gradients '
                             f'of individuals from {r_start} to {r_end}')
        else:
            self.comm.send(start, dest=0, tag=32)
            self.comm.send(end, dest=0, tag=33)
            self.comm.send(self.proc_rank, dest=0, tag=34)
        my_grads = np.empty(((end - start) + 1, self.d), dtype=DTYPE)
        for i, ind in enumerate(self.population[start:end + 1]):
            my_grads[i] = -ind.get_forces().ravel()
        self.comm.Barrier()
        grads = self._gather_gradients(my_grads, start, end)
        self.gradients = grads.copy()
        return grads


class RSFitnessCalculator(FitnessCalculator):
    """ Fitness calculator for Population objects on a restricted
    subspace.

    Parameters
    ----------
    population : Population instance
        the current individual population

    atoms_within_cutoff : list on integers
        the indices of the atoms within the cutoff forming the
        restricted subspace
    """
    def __init__(self, population, atoms_within_cutoff):
        super().__init__(population)
        self.atoms_within_cutoff = atoms_within_cutoff
        self.founder = self.population[0]

    def set_object_parameters(self, x):
        """ Set the object parameters to the individuals in ``self.population``

        Parameters
        ----------
        x : 2D NumPy array
            shape (N, d), with N is the number of individuals in the
            population and d is the dimensionality of the restricted
            subspace of interest.
        """
        N = self.N
        d = len(self.atoms_within_cutoff)*3
        shape = (N, d)
        self._check_input_shape(x, shape)
        long_x = np.tile(self.founder.positions.ravel()[:, np.newaxis], N).T
        for i, index in enumerate(self.atoms_within_cutoff):
            long_x[:, 3*index:3*index + 3] = x[:, 3*i:3*i + 3]
        self.x = long_x
        self._update_population_positions()


class RSFitnessGradientCalculator(RSFitnessCalculator,
                                  FitnessGradientCalculator):
    def get_gradients(self):
        grads = super().get_gradients()
        indices = self.atoms_within_cutoff
        dim = len(indices)*3
        sub_grads = np.empty((len(grads), dim))
        for i, ind in enumerate(indices):
            sub_grads[:, 3*i:3*i + 3] = grads[:, 3*ind:3*ind + 3]
        self.gradients = sub_grads.copy()
        return sub_grads


class MetaRSFitnessCalculator(RSFitnessCalculator):
    """ Calculator for fitness function using a surrogate
    fitness metamodel. The metamodel is used exclusively
    for predicting the total energy. Forces are saved in
    the training dataset, but are not used for train and
    prediction

    Parameters
    ----------
    population : Population instance
        the current individual population

    atoms_within_cutoff : list on integers
        the indices of the atoms within the cutoff forming the
        restricted subspace

    metamodel : ``MetaModel`` instance
        the fitness surrogate

    data : string
        the name of the file which is used to save/read
        the training data. It will be named ``data``.hdf5

    min_generation : int. Default 0
        use the meta-model only in the current generation is
        larger or equal than ``min_generation``

    train_kwargs : dict
        the keyword-argument pairs to train the metamodel
    """
    def __init__(self, population, atoms_within_cutoff,
                 metamodel, data='Xy.hdf5', min_generation=0,
                 train_kwargs=dict()):
        super().__init__(population, atoms_within_cutoff)
        self.metamodel = metamodel
        self.dataset = data
        self.system_name = None
        self.min_generation = min_generation
        self.current_generation = 0
        self.train_kwargs = train_kwargs
        # keep track of individuals in the last generation
        # which will be used to update the training set
        # and their energy
        self.new_training_population = Population()
        self.new_training_population_indices = []
        self.new_energy_train = []
        self.new_forces_train = []
        # STD on predicted energy for those individuals which will be
        # added to the training set
        self.new_energy_std_train = []

        # local containers for individuals which will be added to training set
        self.new_local_training_population_indices = []
        self.new_local_energy_train = []
        self.new_local_forces_train = []
        # keep track for all generations. These data will be used to
        # train the metamodel
        self.training_population = Population()
        self.energy_train = []
        self.forces_train = []

        # Predicted quantities
        # indices individuals accepted from metamodel
        self.local_valid_indices = []
        self.local_predicted_energies = []
        self.local_predicted_energies_std = []

        # Take initial eventual training data
        self.initialize_training_data()
        # eventually train the model
        self.is_fitted = False
        self.train_model()
        self.reset_counts()  # every time the model is trained, one must
                             # reset these counts

    def reset_counts(self):
        self.new_training_population = Population()
        self.new_training_population_indices = []
        self.new_energy_train = []
        self.new_energy_std_train = []
        self.new_forces_train = []

        self.new_local_training_population_indices = []
        self.new_local_energy_train = []
        self.new_local_forces_train = []

        self.local_valid_indices = []
        self.local_predicted_energies = []
        self.local_predicted_energies_std = []

    def initialize_training_data(self):
        try:
            X_data, y_data, dy_data, name, atomic_numbers, cell, pbc = \
                read_train_hdf5(self.dataset)
        except OSError:
            pass
        else:
            if self.proc_rank == 0:
                logger.info('Found an initial dataset with '
                            f'{len(X_data)} instances.')
            with h5py.File(self.dataset, 'r') as f:
                self.system_name = f['system'].attrs['name'].decode()
            N_atoms = len(atomic_numbers)
            for i, X in enumerate(X_data):
                ind = Individual(cell=cell, numbers=atomic_numbers,
                                 pbc=pbc, positions=X.reshape((N_atoms, 3)))
                ind.my_name = 'Train_individual_' + str(i)
                self.training_population.append(ind)
                # update also new training data, so the model will be
                # initialized
                self.new_training_population.append(ind)
            self.energy_train.extend(list(y_data))
            self.forces_train.append(dy_data)
            self.new_energy_train.extend(list(y_data))
            self.new_forces_train.append(dy_data)

    def update_dataset(self):
        if len(self.new_energy_std_train) > 0:
            energy_std = 3*1000*np.array(self.new_energy_std_train)/self.d
        if self.proc_rank == 0:
            names = [self.population[i].my_name
                     for i in self.new_training_population_indices]
            names = '\t'.join(names)
            c1 = len(self.new_energy_std_train) > 0
            c2 = len(self.new_training_population) > 0
            if c1 and c2 and self.is_fitted:  # fitted with predictions
                logger.info(f'Individuals: {names} will be added to the '
                            'training set. The uncertainties on their '
                            f'energies are: {energy_std} meV/atom')
            elif (not self.is_fitted) and c2:  # not fitted
                logger.info(f'Individuals: {names} will be added to the '
                            'training set. These are the first ones to '
                            'be added')
            else:  # fitted with predictions, but no new training data
                if self.current_generation < self.min_generation:
                    logger.info('Predictions using metamodel will start '
                                f'after generation {self.min_generation}')
                    energies = np.array([x.get_total_energy()
                                         for x in self.population])
                    forces = np.vstack([x.get_forces().ravel()
                                        for x in self.population])                    
                    write_train_hdf5(
                        self.dataset, self.population, energies, forces,
                        self.system_name)
                else:
                    logger.info('All individuals were predicted using the '
                                'metamodel. Nothing to add to the '
                                'training data')

            if c2:
                write_train_hdf5(
                    self.dataset, self.new_training_population,
                    self.new_energy_train, self.new_forces_train,
                    self.system_name)

    def train_model(self):
        # retrain only if new instances are added
        if len(self.new_training_population) > 0:
            if self.proc_rank == 0:
                logger.info('Training the metamodel with '
                            f'{len(self.training_population)} instances')
            self.is_fitted = True
            self.metamodel.fit(self.training_population,
                               np.array(self.energy_train),
                               **self.train_kwargs)
            if self.proc_rank == 0:
                logger.info('Metamodel has been trained.')
        # in any case write the descriptors
        else:
            if self.proc_rank == 0:
                self.metamodel.descriptors_database.write_descriptors(
                    self.population) 

    def _local_predict(self):
        """ Local process has to predict energies for its population and
        eventually decide which individuals should be added to the training
        set
        """
        local_pop = self.population[self.p_start:self.p_end + 1]
        if self.is_fitted:
            logger.info(f'Local predictions for process {self.proc_rank}')
            y_pred, y_stds = self.metamodel.predict(local_pop)
            energies = y_pred
            ene_stds = y_stds
            # sometimes gpytorch predicts nan
            ene_stds[np.isnan(ene_stds)] = np.inf
            local_train_bool = 3*ene_stds/self.d >=\
                               self.metamodel.std_value
            logger.info(f'Done local predictions for process {self.proc_rank}')
        else:
            energies = []
            ene_stds = []
            local_train_bool = np.ones(len(local_pop), dtype=bool)
        # This quantity is used only locally
        self.local_valid_indices = np.where(~local_train_bool)[0]

        self.new_local_training_population_indices = \
            np.where(local_train_bool)[0] + self.p_start
        self.local_predicted_energies = energies
        self.local_predicted_energies_std = ene_stds

    def _get_current_training_indices(self):
        # get the indices of the individuals that will be added to
        # the training set plus other info. For getting the training
        # energies, we need that get_fitness is called first

        # this will be empty if no predictions were made
        stds_pred = self.local_predicted_energies_std
        new_indices = self.new_local_training_population_indices
        indices_start = np.array(new_indices) - self.p_start
        if self.proc_rank == 0:
            self.new_training_population_indices.extend(list(new_indices))
            if len(stds_pred) > 0:
                self.new_energy_std_train.extend(
                    list(stds_pred[indices_start]))
            for j in range(1, self.comm_size):
                no_new_indices = self.comm.recv(source=j, tag=11)
                other_indices = np.emtpy(no_new_indices, dtype=np.uint16)
                self.comm.Recv([other_indices, MPI.LONG_INT],
                               source=j, tag=12)
                other_stds = np.empty(no_new_indices, dtype=DTYPE)
                self.comm.Recv([other_stds, MPI.DOUBLE], source=j, tag=13)
                self.new_training_population_indices.extend(
                    list(other_indices))
                self.new_energy_std_train.extend(list(other_stds))
        else:
            self.comm.send(len(new_indices), dest=0, tag=11)
            self.comm.Send([new_indices, MPI.LONG_INT], dest=0, tag=12)
            self.comm.Send(
                [stds_pred[indices_start], MPI.DOUBLE], dest=0, tag=13)
        self.comm.Barrier()
        if self.proc_rank == 0:
            all_new_training_indices = self.new_training_population_indices
        else:
            all_new_training_indices = None
        all_new_training_indices = self.comm.bcast(all_new_training_indices,
                                                   root=0)
        self.new_training_population_indices = all_new_training_indices

    def get_fitness(self):
        self.p_start, self.p_end = self._get_indices_to_process()
        self.current_generation += 1
        if self.current_generation > self.min_generation:
            self._local_predict()
            self.comm.Barrier()
        # update individuals
        start, end = self.p_start, self.p_end
        if self.proc_rank == 0:
            logger.debug(f'The FitnessCalculator in process {self.proc_rank} '
                         f'of {self.comm_size} will calculate the fitness '
                         f'of individuals from {start} to {end}')
            for j in range(1, self.comm_size):
                r_start = self.comm.recv(source=j, tag=32)
                r_end = self.comm.recv(source=j, tag=33)
                logger.debug(f'The FitnessCalculator in process {j} '
                             f'of {self.comm_size} will calculate the fitness '
                             f'of individuals from {r_start} to {r_end}')
        else:
            self.comm.send(start, dest=0, tag=32)
            self.comm.send(end, dest=0, tag=33)

        local_pop = self.population[start:end + 1]
        my_fitnesses = []
        for i in range(start, end + 1):
            if i in self.local_valid_indices:
                ene = self.local_predicted_energies[i]
                self.population[start + i].calc.calculator_results['energy'] =\
                    ene
                self.population[start + i].skip_calc = True
                my_fitnesses.append(-ene)
                std = self.local_predicted_energies_std[i]
                if self.proc_rank == 0:
                    logger.debug(f'Individual {local_pop[i].my_name} fitness '
                                 f'predicted with the metamodel. '
                                 f'STD: {3*1000*std/self.d} meV/atom. '
                                 f'Predicted energy: {ene}')
                    for j in range(1, self.comm_size):
                        other_name = self.comm.recv(source=j, tag=32)
                        other_std = self.comm.recv(source=j, tag=33)
                        other_ene = self.comm.recv(source=j, tag=34)
                        logger.debug(f'Individual {other_name} fitness '
                                     f'predicted with the metamodel. '
                                     f'STD: {3*1000*other_std/self.d} '
                                     'meV/atom. '
                                     f'Predicted energy: {other_ene}')
                else:
                    self.comm.send(local_pop[i].my_name, dest=0, tag=32)
                    self.comm.send(std, dest=0, tag=33)
                    self.comm.send(ene, dest=0, tag=34)
            else:
                ind = self.population[start + i]
                ene = -ind.fitness
                my_fitnesses.append(-ene)
                # add data for training set
                self.new_local_energy_train.append(ene)
                self.new_local_forces_train.append(ind.get_forces().ravel())

        self.comm.Barrier()
        fitnesses = self._gather_fitnesses(my_fitnesses)
        self.fitnesses = np.array(fitnesses)
        self._gather_training_data()
        self.update_dataset()
        self.train_model()
        self.reset_counts()
        return np.array(fitnesses)

    def _gather_training_data(self):
        # population
        self._get_current_training_indices()
        for index in self.new_training_population_indices:
            self.training_population.append(self.population[index])
            self.new_training_population.append(self.population[index])
        # energies and forces
        if self.proc_rank == 0:
            self.new_energy_train.extend(list(self.new_local_energy_train))
            self.new_forces_train.append(self.new_local_forces_train)
            for j in range(1, self.comm_size):
                no_new_indices = self.comm.recv(source=j, tag=41)
                other_energies = np.emtpy(no_new_indices, dtype=DTYPE)
                self.comm.Recv([other_energies, MPI.DOUBLE],
                               source=j, tag=42)
                other_forces = np.empty((no_new_indices, self.d),
                                        dtype=DTYPE)
                self.comm.Recv([other_forces, MPI.DOUBLE], source=j, tag=43)
                self.new_energy_train.extend(list(other_energies))
                self.new_forces_train.append(other_forces)
        else:
            self.comm.send(len(self.new_local_training_population_indices),
                           dest=0, tag=41)
            energies = np.array(self.new_local_energy_train, dtype=DTYPE)
            self.comm.Send([energies, MPI.DOUBLE], dest=0, tag=42)
            forces = np.array(self.new_local_forces_train, dtype=DTYPE)
            forces = np.vstack(forces)
            self.comm.Send([forces, MPI.DOUBLE], dest=0, tag=43)
        self.comm.Barrier()
        self.new_energy_train = self.comm.bcast(self.new_energy_train, root=0)
        self.new_forces_train = self.comm.bcast(self.new_forces_train, root=0)
        self.comm.Barrier()

        self.energy_train.extend(self.new_energy_train)
        self.forces_train.extend(self.new_forces_train)

        self.new_energy_train = np.array(self.new_energy_train)
        self.new_forces_train = np.vstack(self.new_forces_train)

