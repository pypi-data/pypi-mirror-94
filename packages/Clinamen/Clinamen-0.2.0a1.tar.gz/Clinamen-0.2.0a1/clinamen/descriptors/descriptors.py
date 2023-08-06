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
import os

import h5py
from mpi4py import MPI

from dscribe.descriptors import (SOAP, MBTR, LMBTR, ACSF, SineMatrix,
    EwaldSumMatrix)

from clinamen.utils import get_structure_id
from clinamen.descriptors.finger_descriptors_cython import StructureFingerprint
from clinamen.descriptors.utils import write_descriptors, read_descriptors_by_id
from clinamen.evpd import ROOT_LOGGER as logger


COMM_ = MPI.COMM_WORLD
PROC_RANK = COMM_.Get_rank()


class DescriptorsGenerator:
    """ Base class that will produce the desired material descriptors.

    It is expected that one will set the structures for which the descriptors
    will be calculated with :attr:`structures` and then the descriptors for
    these structures can be calculated with :meth:`create_descriptors`.
    """
    available_descriptors = [
        'fingerprints', 'soap', 'mbtr', 'lmbtr', 'acsf', 'sinematrix',
        'esm'
    ]

    descriptors_map = {
        'fingerprints': StructureFingerprint,
        'soap': SOAP,
        'mbtr': MBTR,
        'lmbtr': LMBTR,
        'acsf': ACSF,
        'sinematrix': SineMatrix,
        'esm': EwaldSumMatrix
    }

    def __init__(self, descriptor_name, descriptor_kwargs,
                 creation_kwargs=None):
        """
        Initialize the object that will be used in order to generate the
        descriptors.

        Parameters:
        -----------
        descriptor_name : string
            string that defines the type of descriptors to be used.
            Must be either: 'fingerprints', 'soap', 'mbrt', 'lmbtr', 'acsf',
            'sinematrix', 'esm'

        descriptor_kwargs : dictionary
            keyword-value pairs needed to initialize the descriptor object.
            Each descriptor has its own arguments, so one should check the
            documentation for each descriptor.

        creation_kwargs : dictionary
            optional keyword-value pairs to specify how the descriptors should
            be created. These are the optional parameters used by the
            ``create`` method of a DScribe descriptor object
        """
        self._descriptor_name = descriptor_name
        self._descriptor_kwargs = descriptor_kwargs
        if creation_kwargs is None:
            self._creation_kwargs = dict()
        else:
            self._creation_kwargs = creation_kwargs

        if self._descriptor_name.lower() not in self.available_descriptors:
            raise ValueError(f"Descriptor '{self._descriptor_name}' "
                             "is not available")
        self._descriptor_object = self.descriptors_map[
            self._descriptor_name.lower()]

        # Fingerprint descriptors have different interface
        self._using_fingerprints = (
            True if self.descriptor_name.lower() == 'fingerprints' else False
        )

        self._structures = None

    def _create_descriptors(self, descriptor_creator, atoms):
        if not self._using_fingerprints:
            descriptors = descriptor_creator.create(atoms,
                                                    **self._creation_kwargs)
        else:
            descriptors = descriptor_creator.get_descriptors()
        return descriptors

    def create_descriptors(self):
        """ Create the descriptors for each structure in
        :attr:`self.structures`
        """
        if self.structures is None:
            raise RuntimeError('No structures for which descriptors have to'
                               'be calculated have been given')
        if not self._using_fingerprints:
            init_descriptor = self._descriptor_object(
                **self._descriptor_kwargs)
            for atoms in self.structures:
                yield self._create_descriptors(init_descriptor, atoms)
        else:
            for atoms in self.structures:
                init_descriptor = StructureFingerprint(
                    atoms, **self._descriptor_kwargs)
                yield self._create_descriptors(init_descriptor, atoms)

    @property
    def structures(self):
        """ list of atomic structures for which we want to calculate the
            descriptors
        """
        return self._structures

    @structures.setter
    def structures(self, structures):
        self._structures = structures

    @property
    def descriptor_name(self):
        return self._descriptor_name

    @property
    def descriptor_properties(self):
        return copy.deepcopy(self._descriptor_kwargs)


class DescriptorsDatabase:
    """ Class to manage calculated descriptors """
    def __init__(self, hdf5_filename, initialized_descriptors_generator,
                 tag='descriptors', batch_size=128):
        """
        Parameters:
        -----------
        hdf5_filename : string
            the name of the file where the descriptors have to be read,
            written or appended.
            If a file with name ``hdf5_filename`` already exists, new
            descriptors will be appended.

        initialized_descriptors_generator: :class:`DescriptorsGenerator`
            instance
            The instance used to generate descriptors for the dataset

        tag : string
            the name of the dataset (``dataset.attrs['name']``)

        batch_size : int, default 128
            the number of descriptors to read/write at one time.
            If None, all descriptors will be read/written at once
        """
        self._filename = hdf5_filename

        self.descriptors_generator = initialized_descriptors_generator
        self.tag = tag
        self.batch_size = batch_size

    @property
    def database_exists(self):
        if os.path.isfile(self.filename):
            self._database_exists = True
        else:
            self._database_exists = False
        return self._database_exists
        
    @property
    def filename(self):
        return self._filename
 
    def get_structure_id(self, atoms):
        """ Get the id of an atomic structure

        Parameters:
        -----------
        atoms : ``ase.atoms.Atoms`` instance
            an atomic structure
        """
        positions = atoms.positions.ravel()
        atomic_numbers = atoms.get_atomic_numbers()
        cell = atoms.cell[:].ravel()
        pbc = atoms.pbc
        id_ = get_structure_id(positions, atomic_numbers, cell, pbc)
        return id_

    @property
    def existing_ids(self):
        """ Return a tuple with existing structure ids in the database """
        return self._get_existing_ids()

    def _get_existing_ids(self):
        if not self.database_exists:
            if PROC_RANK == 0:
                logger.debug('No database has been found.')
            return tuple()
        else:
            visited_ids = []
            if PROC_RANK == 0:
                with h5py.File(self.filename, 'r') as f:
                    for val in f['X'].keys():
                        visited_ids.append(val)
            visited_ids = COMM_.bcast(visited_ids, root=0)
            COMM_.Barrier()
            return tuple(visited_ids)

    def write_descriptors(self, structures):
        """ Write a list of atomic structures to the database

        Parameters:
        -----------
        structures: list
            a list of ``ase.atoms.Atoms`` instances of which
            we want to write the descriptors on the database
        """
        indices = np.arange(len(structures))
        no_chunks = int(np.ceil(len(indices)/self.batch_size))
        c_indices = [self.batch_size*i for i in range(1, no_chunks)]
        chunks = np.array_split(indices, c_indices)
        for chunk_no, chunk in enumerate(chunks):
            existing_ids = list(self.existing_ids)
            if PROC_RANK == 0:
                logger.debug(f'Found {len(existing_ids)} existing ids.')
            existing_indices = []
            ids = []
            for indx in chunk:
                id_ = self.get_structure_id(structures[indx])
                if id_ in existing_ids:
                    existing_indices.append(indx)
                else:
                    ids.append(id_)
                    existing_ids.append(id_)
            if PROC_RANK == 0:
                logger.debug(f'{len(ids)} ids to process.')
            ch_structures = [structures[i] for i in chunk
                             if i not in existing_indices]
            if len(ch_structures) != len(ids):
                raise RuntimeError('Length of structures in the batch does '
                                   'not equal the length of the ids')
            self.descriptors_generator.structures = ch_structures
            if PROC_RANK == 0:
                logger.debug(f'Processing chunk {chunk_no + 1}/{len(chunks)}. '
                             f'{len(ids)} descriptors for '
                             f'database: {self.filename}')
                descrs = self.descriptors_generator.create_descriptors()
                array_descrs = []
                for desc in descrs:
                    array_descrs.append(desc.ravel())
                if len(array_descrs) > 0:
                    logger.debug(f'Writing {len(ids)} descriptors to '
                                 f'database: {self.filename}.'
                                 f'{len(existing_indices)} structures were '
                                 'already processed.')
                    array_descrs = np.vstack(array_descrs)
                    write_descriptors(self.filename,
                                      array_descrs, None, ids, self.tag)
                    logger.debug(f'{len(ids)} descriptors have been '
                                 f'written to : {self.filename}')
                else:
                    logger.debug(f'No descriptors to add to '
                                 f'database: {self.filename}')

    def read_descriptors(self, ids=None):
        """ Read the descriptors from the database

        Parameters:
        -----------
        ids : list or None. Default None
            if a list, is a list of identifiers for the structures whose
            descriptors we want to retrieve. If None, all descriptors in
            the database are returned.
        """
        if ids is None:
            ids = self.existing_ids
        else:
            ids = tuple(ids)
        descriptors, jacobians, indices = read_descriptors_by_id(self.filename,
                                                                 ids)
        correct_indices = np.arange(len(descriptors))
        if (correct_indices != indices).any():
            raise RuntimeError('Error: for some reason, descriptors were not '
                               f'read correctly from {self.filename}')
        descriptors = np.vstack(descriptors)
        if jacobians is None:
            return descriptors, None
        else:
            jacobians = np.vstack(jacobians)
            return descriptors, jacobians
