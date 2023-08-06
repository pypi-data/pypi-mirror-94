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
import copy
import numpy as np
import pandas as pd
import os

from mpi4py import MPI

from ase import Atoms
from ase.io.vasp import write_vasp
from ase.calculators.calculator import CalculationFailed

from clinamen.evpd import ROOT_LOGGER as logger
from clinamen.evpd import LOGFILE_NAME
from clinamen.utils import counter

proc_no = MPI.COMM_WORLD.Get_rank()


class Individual(Atoms):
    """ Class for representing an individual in a population.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._total_energy_calculations = 0
        # used to keep track of changes in the structure
        self._atoms_check = None
        # keep track of the original structure
        self._original_structure = Atoms(*args, **kwargs)
        # For cloning instances
        self.calculator_factory = None
        self.calculator_parameters = None
        self.skip_calc = False  # when fitness if produced with metamodel
                                # it must be set to True to avoid another
                                # calculation

    def set_calculator_factory(self, calc_factory, calc_parameters):
        """
        Parameters
        ----------
        calc_factory : a class derived from
            ``ase.calculators.interface.Calculator`` or a function
            generating a calculator

        calc_parameters : dict
            keyword-value pairs used to initialize a ``calc_factory``
            instance
        """
        if callable(calc_factory) or issubclass(calc_factory, type):
            params = copy.deepcopy(calc_parameters)
            calculator = calc_factory(**calc_parameters)
            calculator.calculator_parameters = copy.deepcopy(params)
            calculator.calculator_results = dict()
            self.calculator_factory = calc_factory
            self.calculator_parameters = copy.deepcopy(params)
            super().set_calculator(calculator)
        else:
            raise TypeError('calc_factory must be an object able to '
                            'instantiate a new calculator, i.e. '
                            'either a function or a class')

    @counter
    def get_potential_energy(self, *args, **kwargs):
        attempt_count = 0
        while True:
            try:
                attempt_count += 1
                if proc_no == 0:
                    logger.debug(f'Process {proc_no}: '
                                 'Attempting energy calculation for '
                                 f'individual: {self.my_name}\n'
                                 f'Attempt number: {attempt_count}')
                ene = super().get_potential_energy(*args, **kwargs)
                if proc_no == 0:
                    logger.debug(f'Process {proc_no}: '
                                 f'Energy counter +1 for "{self.my_name}"')

            except CalculationFailed:
                if proc_no == 0:
                    logger.debug(f'Process {proc_no}: '
                                 f'Calculating fitness for '
                                 f'individual {self.my_name} '
                                 'failed. Trying again...')
                continue
            else:
                self._total_energy_calculations += 1
                break
        self.calc.calculator_results['energy'] = ene
        # update
        self._atoms_check = self.copy()
        return ene

    def get_forces(self, *args, **kwargs):
        forces = super().get_forces(*args, **kwargs)
        self.calc.calculator_results['forces'] = forces.copy()
        return forces

    def calculation_required(self):
        """ Returns True if a new energy calculation is required """
        if not self.calc:
            raise RuntimeError('The Individual instance has no '
                               'set calculator')
        try:
            self.calc.calculator_results['energy']
        except KeyError:    # energy was never calculated
            return True
        changes = ['positions', 'cell', 'numbers', 'pbc']
        if self.skip_calc:
            return False
        else:
            for prop in changes:
                value1 = getattr(self, prop)
                value2 = getattr(self._atoms_check, prop)
                if not (value1 == value2).all():
                    return True

    def update_fitness(self):
        """ Calculate the total energy of the individual """
        if proc_no == 0:
            logger.debug(f'Process {proc_no}: '
                         'Calculating fitness of '
                         f'individual "{self.my_name}"')
        if self.calc is not None:
            if self.calculation_required():
                self._fitness = -self.get_potential_energy()
            else:
                if proc_no == 0:
                    logger.debug(f'Process {proc_no}: '
                                 f'{self.my_name} did not change. Using '
                                 'cached fitness')
                self._fitness = -self.calc.calculator_results['energy']
        else:
            if proc_no == 0:
                logger.critical(f'Process {proc_no}: '
                                'Trying to calculate the cost, '
                                f'but the Individual "{self.my_name}" '
                                'instance has no calculator')
            raise RuntimeError('The Individual instance has no '
                               'set calculator')

    @property
    def cost(self):
        """ Value of the cost function of the individual (its energy) """
        return -self.fitness

    @property
    def fitness(self):
        """ Fitness value of the individual """
        self.update_fitness()  # this will initialize self._fitness
        if hasattr(self, '_fitness_transformed'):
            return self._fitness_transformed
        return self._fitness

    @property
    def defect_position(self):
        """ Location of the eventual defect in the structure """
        return self._defect_position

    @defect_position.setter
    def defect_position(self, value):
        """ Scaled positions of the defective site """
        if isinstance(value, (list, tuple, np.ndarray)):
            self._defect_position = np.array(value)
        else:
            if proc_no == 0:
                logger.exception(f'Process {proc_no}: '
                                 'The defect position is required, but '
                                 f'the Individual "{self.my_name}" '
                                 'instance has no set defect position.')
            raise TypeError('Defect position must be given as a 1D array')

    @property
    def metric_tensor(self):
        """ The metric tensor of the cell """
        cell = self.get_cell()[:]
        metric = np.dot(cell, cell.T)
        return metric

    @property
    def distances_from_defect(self):
        """ Distance of each atom in the system from the defect """
        self._distances_from_defect = self._get_distances_from_defect()
        return self._distances_from_defect
    
    @property
    def my_name(self):
        """ Identifier """
        if not hasattr(self, '_my_name'):
            self._my_name = 'individual'
        return self._my_name

    @my_name.setter
    def my_name(self, value):
        self._my_name = value

    @property
    def etol(self):
        """ Tolerance for comparing costs between two individuals """
        return self._etol

    @etol.setter
    def etol(self, value):
        self._etol = value

    @property
    def drel(self):
        r""" Tolerance for the relative distance between two individuals.
        The relative distance is defined as:

        .. math::

            d_{rel}(i, j) = \frac{\sum_k |d_i(k) - d_j(k)|}{\sum_k d_i(k)}
            
        """
        return self._drel

    @drel.setter
    def drel(self, value):
        self._drel = value

    @property
    def dmax(self):
        """ Tolerance for the maximum distance discrepancy
        between two individuals.
        This distance is defined as:

        .. math::

            d_max(i, j) = max_k(|d_i(k) - d_j(k)|)
            
        """
        return self._dmax

    @dmax.setter
    def dmax(self, value):
        self._dmax = value

    @property
    def dmin(self):
        """ Tolerance for the minimum distance at which two atoms
        can be located. Used to reject a structure where two atoms
        are too close. 

        Default value = 0.25 minimum bond length in the system
        """
        if hasattr(self, '_dmin') and self._dmin is not None:
            return self._dmin
        distances = self._original_structure.get_all_distances(mic=True)
        mindist = distances[0][1:]
        mindist = np.min(mindist)
        self._dmin = 0.25*mindist
        return self._dmin

    @dmin.setter
    def dmin(self, value):
        self._dmin = value

    @property
    def chromosome(self):
        """ The chromosome of an individual is the set of displacements
        from an initial configuration. Usually one very similar to the
        pristine system
        """
        chromosome = self.positions - self._original_structure.positions
        return chromosome

    @property
    def total_energy_calculations(self):
        """ Number of times the energy of the individual has been calculated
        """
        return self._total_energy_calculations

    @property
    def data(self):
        positions = [['x' + str(i), 'y' + str(i), 'z' + str(i)]
                     for i in range(len(self))]
        positions = [tag for sublist in positions for tag in sublist]
        data_pos = self.positions.ravel()
        displacements = [['dx' + str(i), 'dy' + str(i), 'dz' + str(i)]
                         for i in range(len(self))]
        displacements = [tag for sublist in displacements for tag in sublist]
        try:
            data_disp = self.chromosome.ravel()
        except AttributeError:
            data_disp = np.zeros_like(data_pos)
        lpos = ['Positions']*len(positions)
        lchrom = ['Chromosome']*len(displacements) 
        level1 = lpos + lchrom
        level1.extend(['Fitness']*2)
        level2 = positions + displacements
        level2.extend(['From Energy', 'Actual'])
        index = pd.MultiIndex.from_arrays([level1, level2])
        data = list(data_pos)
        data.extend(list(data_disp))
        if not self.calculation_required():
            transformed_fitness = self.fitness #update fitness if needed
            from_energy = self._fitness
            data.extend([from_energy, transformed_fitness])
        else:
            data.extend([np.nan, np.nan])
        series = pd.Series(index=index, data=data, dtype=np.float,
                           name=self.my_name)
        return series

    @property
    def founder(self):
        if hasattr(self, '_founder'):
            return self._founder
        founder_atoms = self._original_structure
        founder = Individual.make_individual_from_ase_atoms(founder_atoms)
        if hasattr(self, '_defect_position'):
            founder.defect_position = self.defect_position.copy()
        founder.my_name = self.my_name + '_founder'
        if hasattr(self, '_etol'):
            founder.etol = self.etol
        if hasattr(self, '_drel'):
            founder.drel = self.drel
        if hasattr(self, '_dmax'):
            founder.dmax = self.dmax
        if hasattr(self, '_dmin'):
            founder.dmin = self.dmin
        founder._original_structure = self._original_structure.copy()
        if proc_no == 0:
            logger.debug(f'Process {proc_no}: '
                         f'Founder  "{founder.my_name}" created')
        self._founder = founder
        return self._founder

    def has_proper_structure(self):
        """ Returns False if any interatomic distance in the system is
        smaller than ``self.dmin``.
        """
        distances = self.get_all_distances(mic=True)
        #remove diagonal elements
        vdistances = distances[~np.eye(distances.shape[0],dtype=bool)]
        return (vdistances > self.dmin).all()

    def _get_distances_from_defect(self):
        """ Calculate the distance of each atom in the cell from the defect
        site using PBCs """
        def_pos = self.defect_position
        positions = self.get_scaled_positions()
        cell = self.get_cell()[:]
        diff_pos = positions - def_pos
        diff_pos -= np.rint(diff_pos)
        metric = self.metric_tensor
        distances = np.diag(np.dot(diff_pos, np.dot(metric.T, diff_pos.T)))
        return np.sqrt(distances)

    def _get_distances_from_origin(self):
        scaled_pos = self.get_scaled_positions()
        scaled_pos -= np.rint(scaled_pos)
        metric = self.metric_tensor
        distances = np.diag(np.dot(scaled_pos, np.dot(metric.T, scaled_pos.T)))
        return np.sqrt(distances)

    def write_poscar(self, path=None):
        """ If path is not None, it is the folder where the POSCAR file
        will be saved
        """
        filename = 'POSCAR_' + self.my_name
        if path:
            filename = os.path.join(path, filename)
        write_vasp(filename, self, direct=True, sort=None, vasp5=True)
        if proc_no == 0:
            logger.info(f'Process {proc_no}: '
                        f'Individual "{self.my_name}" configuration '
                        'saved as POSCAR file '
                        f'with name: "{filename}"')

    def clone(self):
        """ Copy the instance, return a new instance """
        if proc_no == 0:
            logger.debug(f'Process {proc_no}: '
                         f'Creating clone of Individual "{self.my_name}"')
        copied_item = Individual.make_individual_from_ase_atoms(self)
        copied_atoms = self.copy()
        copied_original = self._original_structure.copy()
        copied_item._original_structure = copied_original
        copied_item._atoms_check = copied_atoms
        copied_item.set_calculator_factory(self.calculator_factory,
                                           self.calculator_parameters)
        if hasattr(self, '_fitness'):
            copied_item.calc.calculator_results['energy'] = \
                self.calc.calculator_results['energy']
            try:
                copied_item.calc.calculator_results['forces'] = \
                    self.calc.calculator_results['forces'].copy()
            except KeyError:
                pass
        if hasattr(self, '_defect_position'):
            copied_item.defect_position = self.defect_position.copy()
        copied_item.my_name = self.my_name + '_clone'
        if hasattr(self, '_etol'):
            copied_item.etol = self.etol
        if hasattr(self, '_drel'):
            copied_item.drel = self.drel
        if hasattr(self, '_dmax'):
            copied_item.dmax = self.dmax
        if hasattr(self, '_dmin'):
            copied_item.dmin = self.dmin
        if hasattr(self, '_fitness'):
            copied_item._fitness = self._fitness
        if hasattr(self, '_fitness_transformed'):
            copied_item._fitness_transformed = self._fitness_transformed
        if proc_no == 0:
            logger.debug(f'Process {proc_no}: '
                         f'Clone  "{copied_item.my_name}" created')
        return copied_item

    def calculate_comparison_distances(self, other):
        """ Calculates the relative distance and the maximum distance
        discrepancy between this individual and another one.

        Parameters
        ----------
        other : Individual instance

        Return
        ------
        rel_dist, max_dist : the relative and maximum discrepancy 
            distance between the two instances
        """
        d_1 = self._get_distances_from_origin()
        d_2 = other._get_distances_from_origin()
        diff = np.abs(d_1 - d_2)
        num = diff.sum()
        den = np.sum(d_1)
        return num/den, np.max(diff)

    def optimize_structure(self, **kwargs):
        """ Optimize the structure

        Parameters
        ----------
        kwargs : dict
            parameters for running the geometry optimization.
            A mandatory key is `optimizer`, which is an ase optimizer.
            The other key:value pairs are the parameters to supply to
            `optimizer`.
        """
        if proc_no == 0:
            logger.info(f'Process {proc_no}: '
                        'Optimizing structure of '
                        f'individual "{self.my_name}"')
        optimizer = kwargs.pop('optimizer', None)
        if optimizer is None:
            raise ValueError('An optimizer should be given for '
                             'optimizing the structure')
        with open(LOGFILE_NAME, 'a') as fileobj:
            optimizer = optimizer(self, logfile=fileobj)
            optimizer.run(**kwargs)
        if proc_no == 0:
            logger.info(f'Process {proc_no}: Optimization completed')

    @staticmethod
    def make_individual_from_ase_atoms(atoms):
        """ Takes an ase.Atoms instance and returns
        an evpd.core.Individual instance.

        The result is analogous to using ``atoms.copy()``,
        but also the calculator will be copied.
        """
        if not isinstance(atoms, Atoms):
            raise TypeError('The function argument is not '
                            'an ase.Atoms instance')
        if proc_no == 0:
            logger.debug(f'Process {proc_no}: '
                         'Generating an Individual from '
                         'an Atoms object')
        cell = atoms.cell[:].copy()
        pbc = atoms.pbc.copy()
        celldisp = atoms._celldisp.copy()
        info = atoms.info.copy()
        individual = Individual(cell=cell, pbc=pbc,
                                celldisp=celldisp, info=info)
        individual.arrays = dict()
        for key, value in atoms.arrays.items():
            individual.arrays[key] = value.copy()
        individual.constraints = copy.deepcopy(atoms.constraints)

        individual._original_structure = atoms.copy()

        return individual
