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
import numpy as np

import h5py

from clinamen import DESCRIPTORS_FLOAT_DTYPE as DTYPE


def write_descriptors(file_name, descriptors, descriptors_grads, ids,
                      name=None, flattened=True):
    """ Append new data to an existing dataset, if the dataset
    does not exist, create a new one

    Parameters
    ----------
    file_name : string
        the dataset name

    descriptors : 2D array-like of shape (n, d), if :attr:`flattened` is ``True``.
        n is the number of structures for which the descriptors
        were calculated. d is the dimensionality of the descriptors.
        If :attr:`flattened` is ``False``, descriptors can be a multidimensional
        array of shape (n, ...). 

    descriptors_grads : 2D array-like of shape (n, r) if :attr:`flattened` is ``True``.
        Otherwise, it can be a multidimensional array of shape (n, ...).
        It can also be ``None``. If not None, these are the (possibly flattened,
        if :attr:`flattened` is ``True``) Jacobians of the descriptors.

    name : string. Default None
        the system name. A tag that specifies the system when the
        dataset is created. If the dataset already exists, it checks
        the it corresponds to system ``name``

    ids : array-like of shape (n, )
        for each descriptor, is a string that identifies the structure
        coresponding to that descriptor
    """
    comp_kwargs = {'compression': 'gzip', 'compression_opts': 9}
    descriptors = np.atleast_2d(descriptors)
    if flattened:
        d = descriptors.shape[1]
        shape_x = (d, )
    else:
        d = descriptors.shape[1:]
        shape_x = d
    X = descriptors.copy()
    n_structs = X.shape[0]
    if n_structs != len(ids):
        raise ValueError(f'Have got descriptors for {n_structs} structures '
                         f'but {len(ids)} identifiers are given')
    shape_dx = tuple()
    if descriptors_grads is not None:
        descriptors_grads = np.atleast_2d(descriptors_grads)
        if flattened:
            r = descriptors_grads.shape[1]
            shape_dx = (r, )
        else:
            r = descriptors_grads.shape[1:]
            shape_dx = r
        DX_shape = descriptors_grads.shape
        DX = descriptors_grads.copy()
        if X.shape[0] != DX.shape[0]:
            raise ValueError(f'Have got descriptors for {X.shape[0]} '
                             f'structures but gradients for {DX.shape[0]}')
    new_dataset = True
    if os.path.isfile(file_name):
        new_dataset = False
        # get data to check dataset consistency
        with h5py.File(file_name, 'r') as f:
            sys_name = f['system'].attrs['name'].decode()
            existing_X_shape = tuple(f['system'].attrs['X_shape'])
            existing_DX_shape = tuple(f['system'].attrs['dX_shape'])
        if name is not None:
            c0 = (name == sys_name)
        else:
            c0 = True
        if not c0:
            raise ValueError(f'Dataset name tag {name} does not '
                             f'agree with the name tag {sys_name} '
                             f'of dataset {file_name}')
        if existing_X_shape != shape_x:
            raise ValueError(f'Descriptors have shape {shape_x}, but '
                             f'existing descriptors with shape '
                             f'{existing_X_shape} have been found in '
                             f'{file_name}')
        c1 = existing_DX_shape != shape_dx
        c2 = existing_DX_shape is not tuple()
        c3 = shape_dx is not tuple()
        if (c1 and c2) or (c1 and c3):
            raise ValueError(f'Descriptors Jacobians have shape {shape_dx}, '
                             f'but existing Jacobians with shape '
                             f'{existing_dX_shape} have been found in '
                             f'{file_name}')
    if new_dataset:
        with h5py.File(file_name, 'w') as f:
            system = f.create_group('system')
            if name is None:
                sys_name = 'system'
            else:
                sys_name = name
            system.attrs['name'] = np.string_(sys_name)
            system.attrs['X_shape'] = np.array(shape_x, dtype=np.uint16)
            system.attrs['dX_shape'] = np.array(shape_dx, dtype=np.uint16)
            dataX = f.create_group('X')
            dataX.attrs['name'] = np.string_('descriptors')
            for desc, struct_id in zip(X, ids):
                dataX.create_dataset(struct_id, data=desc, dtype=DTYPE,
                                     maxshape=shape_x, **comp_kwargs)
            if descriptors_grads is not None:
                dataDX = f.create_group('DX')
                dataDX.attrs['name'] = np.string_('descriptors_Jacobians')
                for desc_grad, struct_id in zip(DX, ids):
                    dataDX.create_dataset(struct_id, data=desc_grad,
                                          dtype=DTYPE,
                                          maxshape=shape_dx, **comp_kwargs)
    else:
        with h5py.File(file_name, 'a') as f:
            dataX = f['X']
            for desc, struct_id in zip(X, ids):
                if struct_id in dataX.keys():
                    continue
                dataX.create_dataset(struct_id, data=desc, dtype=DTYPE,
                                     maxshape=shape_x, **comp_kwargs)
            if descriptors_grads is not None:
                dataDX = f['DX']
                for desc_grad, struct_id in zip(DX, ids):
                    dataDX.create_dataset(struct_id, data=desc_grad,
                                          dtype=DTYPE,
                                          maxshape=shape_dx, **comp_kwargs)


def read_descriptors_by_id(file_name, ids):
    """ Given an id or a list thereof, it returns the eventual descriptors
    and Jacobians

    Parameters
    ----------
    file_name : string
        the hdf5 file from where the descriptors should be fetched

    ids : iterable
        the identity keys of the descriptors we want to fetch

    Returns
    -------
    X, DX indices: tuple
        the descriptors and their Jacobians, each as a list, and a list
        representing the indices corresponding to the ids in ``ids`` that
        were found.
        If the Jacobians are not present, None is returned
    """
    indices = []
    if not os.path.isfile(file_name):
        return None, None, []

    with h5py.File(file_name, 'r') as f:
        dataX = f['X']
        grads = True
        try:
            dataDX = f['DX']
        except KeyError:
            grads = False
        X_data = []
        DX_data = []
        for i, id_no in enumerate(ids):
            try:
                val = np.array(dataX[id_no], dtype=DTYPE)
            except KeyError:
                continue
            else:
                indices.append(i)
                X_data.append(val)
                if grads:
                    DX_data.append(np.array(dataDX[id_no], dtype=DTYPE))
        if grads:
            if len(X_data) != len(DX_data):
                raise ValueError(f'Found {len(X_data)} descriptors instances '
                                 f'but {len(DX_data)} Jacobians')
        if len(X_data) == 0:
            X_data = None
        if len(DX_data) == 0:
            DX_data = None
        return X_data, DX_data, indices
