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
import os
import json
import numpy as np
import hashlib
import h5py

from ase.io.vasp import write_vasp
from ase.atoms import Atoms
from ase.io.trajectory import Trajectory

from clinamen import DESCRIPTORS_FLOAT_DTYPE as DTYPE


def counter(function):
    function._callcount = 0
    def decorated(*args, **kwargs):
        function._callcount += 1
        decorated.count = function._callcount
        return function(*args, **kwargs)
    return decorated


class GeneralizedEncoder(json.JSONEncoder):
    """ Simple encoder class that allows np.ndarrays
    encoding by using the array tolist() method
    """
    def default(self, o):
        if isinstance(o, np.ndarray):
            return o.tolist()
        return json.JSONEncoder.default(self, o)


def get_structure_id(positions, atomic_numbers, cell, pbc):
    """ Obtain an (quasi)unique identifier given an atomic structure

    Parameters
    ----------
    positions: 1D array of shape (n_atoms*3, )
        the flattened atomic positions

    atomic_numbers: 1D array of shape (n_atoms, )
        the atomic numbers identifying the atoms in the system

    cell: 1D numpy array of shape (9, )
        the flattened unit cell vectors

    pbc: 1D array of bools of shape (3, )
       each entry determines if pbc are applied to that direction

    Returns
    -------
    hashed : string
        the string digest of the hash function associated to this
        atomic structure
    """
    no_dec = 10
    dt = '<f8'
    m = hashlib.sha256()
    positions = np.array(positions, dtype=dt).round(no_dec)
    atomic_numbers = np.array(atomic_numbers, dtype='<u1')
    cell = np.array(cell, dtype=dt).round(no_dec)
    pbc = np.array(pbc, dtype='<u1')
    if positions.ndim != 1:
        raise ValueError('Atomic positions must be given as a 1D array')
    if atomic_numbers.ndim != 1:
        raise ValueError('Atomic numbers must be given as a 1D array')
    if cell.ndim != 1 or len(cell) != 9:
        raise ValueError('Unit cell must be given as a 1D array '
                         'with 9 entries')
    if pbc.ndim != 1 or len(pbc) != 3:
        raise ValueError('PBC must be given as a 1D array with 3 entries')
    no_atoms = len(atomic_numbers)
    if not len(positions) == 3*no_atoms:
        raise ValueError(f'The structure has {no_atoms} atoms, but '
                         'the atomic positions describe '
                         f'{len(positions)//3} atoms')

    structure_id = [positions, atomic_numbers, cell, pbc]
    structure_id = np.concatenate(structure_id)

    m.update(structure_id.tostring(order='C'))
    hashed = m.hexdigest()

    return hashed


def get_id(atoms):
    """ Return the id of the structure.

    Parameters
    ----------
    atoms : ase.Atoms instance
        the structure whose id has to be calculated

    Returns
    -------
    id_ : string
        the id of the structure
    """
    positions = atoms.positions.ravel()
    atomic_numbers = atoms.get_atomic_numbers()
    cell = atoms.cell[:].ravel()
    pbc = atoms.pbc
    id_ = get_structure_id(positions, atomic_numbers, cell, pbc)
    return id_


def make_atoms(cell, numbers, positions, pbc):
    """ Return an ase.Atoms instance from structural data

    Parameters
    ----------
    cell : 3x3 array
        the Cartesian coordinates of the structure cell

    numbers : 1D array of length N
        the atomic numbers of the atoms in the structure

    positions : 2D array of shape (N, 3)
        the Cartesian positions of the atoms in the system

    pbc : 1D array of 3 bools
        whether pbc are applied along each of the 3 dimensions

    Returns
    -------
    atoms : ase.Atoms instance
        the Atoms object representing the structure
    """
    atoms = Atoms(cell=cell, numbers=numbers, positions=positions,
                  pbc=pbc)
    return atoms


def generate_fingerprints(traj_filename, descr_kwargs, verbose=True):
    """ For each structure in a .traj file calculates the structure
    fingerprints descriptors according to ``descr_kwargs``

    Parameters
    ----------
    traj_filename : string
        the path where the .traj file is located

    descr_kwargs: dict
        the key:value pairs needed to initialize a StructureFingerprint
        instance

    verbose : bool. Default True
        if True, the function will print the progress of the calculation

    Returns
    -------
    descriptor_name : string
        the name of the hdf5 file where the descriptors are written.

    Notes
    -----
    The function will write the text file:
    visited_ids.txt : List of structure ids already visited.
    If the function is interrupted, it will read this file to see
    for which structures features were already calculated
    """
    descriptor_name = [str(descr_kwargs[x]) for x in descr_kwargs.keys()]
    descriptor_name = '_'.join(descriptor_name)
    ids = []
    feats = []
    traj_file = Trajectory(traj_filename)
    tot = len(traj_file)
    unique_structs = 0
    if os.path.isfile('visited_ids.txt'):
        visited_ids = []
        with open('visited_ids.txt', 'r') as f:
            for line in f:
                visited_ids.append(line.strip())
    else:
        visited_ids = []
    for i, atoms in enumerate(traj_file):
        if verbose:
            print(f'Structure {i}/{tot}')
        id_ = get_id(atoms)
        if id_ in visited_ids:
            continue
        if verbose:
            print('id: ', id_)
            print(len(atoms))
        if id_ in ids:
            if verbose:
                print('The structure has already been visited')
            xx = np.where(np.array(ids) == id_)[0]
            if verbose:
                print(f'Is the structure of system {xx}')
        else:
            unique_structs += 1
            feat = StructureFingerprint(atoms, **descr_kwargs).get_descriptors()
            if verbose:
                print(f'Number of features: {len(feat)}')
            ids.append(id_)
            feat = np.atleast_2d(feat)
            write_descriptors('finger_descriptors' + descriptor_name + '.hdf5',
                              feat, None, [id_], 'clustering_set')
            with open('visited_ids.txt', 'a') as f:
                f.write(id_ + '\n')
            if verbose:
                print('Written')
    return descriptor_name


def generate_evolution_trajectory(evolution_history, traj_filename):
    """ From a evolution history hdf5 file, generate the evolution
    trajectory. Note that the individuals are sorted by generation.
    Starting with the Founder

    Parameters
    ----------
    evolution_history : string
        the path to the evolution_history.hdf5 file

    traj_filename : string
        the name of the .traj file to be generated    

    Notes
    -----
    The function will write the text file:
    mapping_ids_structure_names.txt
    The first column has the structure name, as read from
    ``evolution_history`` and the second column the corresponding structure id
    """
    if os.path.isfile(traj_filename):
        print(f'File {traj_filename} already exists')
    else:
        print(f'Creating {traj_filename}')
        structs = []
        structs_names = []
        structs_ids = []
        with h5py.File(evolution_history, 'r') as f:
            cell = np.array(f['system']['cell'])
            numbers = np.array(f['system']['atomic_numbers'])
            pbc = np.array(f['system']['pbc']).astype(bool)
            no_atoms = len(numbers)
            all_keys = []
            for key in f.keys():
                if key != 'system':
                    all_keys.append(key)
            gen_indices = [int(x.split('_')[1]) for x in all_keys]
            sorting_ind = np.argsort(gen_indices)
            all_keys = np.array(all_keys)[sorting_ind]
            for key in all_keys:
                gen_positions = np.array(f[key]['positions'])
                for positions, label in zip(gen_positions,
                                            np.array(f[key]['labels'])):
                    positions = positions.reshape((no_atoms, 3))
                    atoms = make_atoms(cell, numbers, positions, pbc)
                    structs.append(atoms)
                    structs_names.append(label.decode())
                    structs_ids.append(get_id(atoms))

        all_traj = Trajectory(traj_filename, 'a')
        for struct in structs:
            all_traj.write(struct)
        all_traj.close()

        print('Creating mapping file')
        mapping = open('mapping_id_structure_names.txt', 'w')
        for i_name, id_ in zip(structs_names, structs_ids):
            mapping.write(i_name + '\t' + id_ + '\n')
        mapping.close()


def retrieve_structures_names_and_ids_from_file(mapping_file):
    """ Read a mapping file and retrieve the pairs of strucure ids and
    structure names.

    Parameters
    ----------
    mapping_file : string
        The path to a text file containing structure names on the first
        column and corresponding structure ids on the second one

    Returns
    -------
    structures, ids : tuple
		the first is a list of structure names and the second a list of
		corresponding ids
	    """
    structures = []
    ids = []
    with open(mapping_file, 'r') as f:
        for line in f:
            struct, id_ = line.strip().split()
            structures.append(struct) 
            ids.append(id_)
    return structures, ids


def get_descriptors(file_name, mapping_file):
    """ Read a hdf5 file containing the descriptors for some structures.

    Parameters
    ----------
    file_name : string
        path to the hdf5 file containing the calculated descriptors

    mapping_file : string
        The path to a text file containing structure names on the first
        column and corresponding structure ids on the second one

    Returns
    -------
    descriptors, ordered_structures : tuple
        The first element is a 2D array with the descriptors. Each row
        represents a structure. The second file is a 1D array with the
        corresponding structure names.
    """
    structures, ids = retrieve_structures_names_and_ids_from_file(mapping_file)
    descriptors = []
    ordered_structures = []
    structures = np.array(structures)
    with h5py.File(file_name, 'r') as f:
        dataX = f['X']
        for id_ in dataX.keys():
            index = np.where(np.array(ids) == id_)[0]
            structure = structures[index]
            assert len(structure) == 1
            ordered_structures.append(structure[0])
            descriptors.append(np.array(dataX[id_], dtype=DTYPE))
        print(f'Found {len(descriptors)} structures')

    descriptors = np.vstack(descriptors)
    
    return descriptors, np.array(ordered_structures)
