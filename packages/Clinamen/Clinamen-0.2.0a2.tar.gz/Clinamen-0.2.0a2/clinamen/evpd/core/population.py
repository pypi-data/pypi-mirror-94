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
from collections.abc import MutableSequence
import numpy as np
import pandas as pd

from clinamen.evpd import ROOT_LOGGER as logger
from clinamen.evpd.core.individual import Individual


class BadPopulationMember(Exception):
    """ Raise the exception when one tries to add to a ``Population``
    instance an object which is not an ``Individual`` instance
    """
    pass


class Population(MutableSequence):
    """ A population is a group of individual of a given size.

    Parameters
    ----------
    individuals : a list or tuple of individuals.
        the container of individuals forming the population.
        It can also be a single individual or empty.
    """
    def __init__(self, *individuals): 
        self._individuals = []
        # passing variable number of arguments
        if hasattr(individuals, '__iter__') and len(individuals) > 1:
            for ind in individuals:
                self._check_type(ind)
                self._individuals.append(ind)
        # empty
        elif hasattr(individuals, '__iter__') and len(individuals) == 0:
            pass
        # passing a list or tuple
        elif ((isinstance(individuals[0], tuple) 
              or isinstance(individuals[0], list)) and len(individuals) == 1):
            for ind in individuals[0]:
                self._check_type(ind)
                self._individuals.append(ind)
        # single element
        elif len(individuals) == 1:
            self._check_type(individuals[0])
            self._individuals.append(individuals[0])
        else:
            self._check_type(individuals)
            self._individuals.append(individuals)
        
    def _check_type(self, obj):
        if not isinstance(obj, Individual):
            raise BadPopulationMember('Only instances of type Individual can '
                                      'be part of a Population instance')

    def __len__(self):
        return len(self._individuals)
 
    def __getitem__(self, key):
        """ Return another Population instance if key is a slice.
        Note that the individuals are not copied, similar behavior of a
        ``list``"""
        if isinstance(key, slice):
            return self.__class__(self._individuals[key])
        else:
            return self._individuals[key]

    def __setitem__(self, key, value):
        isiter = hasattr(value, '__iter__')
        if isinstance(key, int) and isinstance(value, Individual):
            self._individuals[key] = value
            logger.info('Individual number "{}" has been replaced'.format(key))
        elif isinstance(key, slice) and isiter:
            for i, individual in enumerate(value):
                self._check_type(individual)
                step = key.step if key.step else 1
                self._individuals[key.start + i * step] = individual 
            logger.info('Individuals "{}" have been '
                        'replaced'.format(':'.join([str(key.start),
                                                    str(key.stop),
                                                    str(key.step)])))
        else:
            self._check_type(value)
 
    def __delitem__(self, key):
        if isinstance(key, (int, slice)):
            del self._individuals[key]
        else:
            raise TypeError('Indices must be integers or slices')

    def insert(self, index, value):
        isseq = hasattr(value, '__len__') and hasattr(value, '__getitem__')
        if isseq and isinstance(value, Individual): # Individuals are iterables
            pass
        elif isseq: # another iterable
            for individual in value:
                self._check_type(individual)
        else:
            self._check_type(value)
        if isinstance(index, int):
            self._individuals.insert(index, value)
        else:
            raise TypeError('The index must be an integer')

    @property
    def individuals_fitness(self):
        """ Return a list with the fitness of each individual """
        self._individuals_fitness = [x.fitness for x in self]
        return self._individuals_fitness

    @property
    def dataframe(self):
        data = [x.data for x in self]
        df = pd.DataFrame(data=data)
        df.rename_axis('Name', inplace=True)
        df.reset_index(inplace=True)
        df.index = df.index.map(int)
        return df
        
    def sort(self):
        fitnesses = self.individuals_fitness
        indices = np.argsort(fitnesses)
        old_ind = self._individuals[:]
        for i, index in enumerate(indices):
           self._individuals[i] = old_ind[index]

    def get_equal_individuals(self):
        keys = [x.my_name for x in self]
        equals = {}
        for i, ind in enumerate(self):
            if ind.my_name in keys:
                equals[ind.my_name] = []
                keys.remove(ind.my_name)
                for ind2 in self[i+1:-1]:
                    if ind == ind2:
                        equals[ind.my_name].append(ind2.my_name)
                        keys.remove(ind2.my_name)
        return equals
