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
from itertools import combinations_with_replacement
import numpy as np
cimport numpy as cnp
from scipy.spatial.distance import cdist
cimport cython
from math import ceil
from libc.math cimport floor, erf, sqrt, pow, exp
from libc.stdlib cimport malloc, free

import ase.atoms

from mpi4py import MPI
from clinamen.evpd import ROOT_LOGGER as logger
from clinamen import DESCRIPTORS_FLOAT_DTYPE as DTYPE

#ctypedef cnp.float32_t DTYPE_t


cdef inline _add_positions(double [::1] v1, double [::1] v2,
                           double [::1] res, int n):
    cdef Py_ssize_t i
    for i in range(n):
        res[i] = v1[i] + v2[i]


cdef inline _subtract_positions(double [::1] v1, double [::1] v2,
                                double [::1] res, int n):
    cdef Py_ssize_t i
    for i in range(n):
        res[i] = v1[i] - v2[i]


cdef inline double _calculate_distance(double [::1] v1,
                                        double [::1] v2, int n):
    cdef Py_ssize_t i
    cdef double distance = 0
    for i in range(n):
        distance += pow(v1[i] - v2[i], 2)
    return sqrt(distance)


cdef inline double ** allocate_memory_2d_array(size_t n_rows, size_t n_cols):
    cdef size_t i
    cdef double **array = <double **> malloc(n_rows*sizeof(double *))
    if array is NULL:
        raise MemoryError()
    for i in range(n_rows):
        array[i] = <double *> malloc(n_cols*(sizeof(double)))
        if array[i] is NULL:
            raise MemoryError()
    return array

cdef inline void free_memory_2d_array(double **array, size_t n_rows):
    cdef size_t i
    for i in range(n_rows):
        free(array[i])
    free(array)
    
cdef inline void zero_2d_array(double **array, size_t n_rows, size_t n_cols):
    cdef size_t i
    cdef size_t j

    for i in range(n_rows):
        for j in range(n_cols):
            array[i][j] = 0


cdef extern from "finger_descriptors_c.h":
    void calculate_radial_fingerprints_a_b(double **positions_a,
                                           double **positions_b,
                                           double **translations,
                                           size_t na, size_t nb,
                                           size_t nt, double tol,
                                           double smearing, double bin_size,
                                           double volume, double r_max,
                                           double *fingerprint_a_b,
                                           size_t bin_number)

    void calculate_radial_fingerprint_gradient_a_b(double **positions_a,
                                                   double **positions_b,
                                                   unsigned short *indices_a,
                                                   unsigned short *indices_b,
                                                   double **translations,
                                                   size_t na, size_t nb,
                                                   size_t nt, double tol,
                                                   double smearing,
                                                   double bin_size,
                                                   double volume, double r_max,
                                                   double **fingerprint_grad_a_b,
                                                   size_t dofs,
                                                   size_t bin_number)



class StructureFingerprint:
    """ Basic implementation of the structure fingerprint of Oganov and Valle

    Parameters
    ----------
    structure : (sub)instance of ``ase.atoms.Atoms`` object
        the structure to which the fingerprint has to be calculated

    r_max : float. Default None: r_max is set to 1.5 times the largest
            diagonal of the cell.
        maximum radial distance used for the fingerprint

    smearing : float. Default 0.2 Angstrom
        the smearing to be used by the Gaussian kernel. In Angstrom

    bin_size : float. Default 0.05 Angstrom
        the bin size used to discretize the function fingerprint

    bin_number : int. Default None
        the number of bin used to discretize the fingerprint function

    pure_c : bool. Default True
        use pure C functions to calculate the fingerprints

    Notes
    -----
    If both ``bin_size`` and ``bin_number`` are not None,
    only ``bin_number`` is used. To use ``bin_size``, set
    ``bin_number`` to None.
    """
    def __init__(self, structure, r_max=None,
                 smearing=0.2, bin_size=0.05, bin_number=None, pure_c=True):
        self._atoms = structure
        if r_max is None:
            diags = self._find_length_cell_diagonals()
            self.r_max = 1.5*np.max(diags)
        else:
            self.r_max = r_max
        self.smearing = smearing
        # tolerance to use for the gaussian integrals
        self.tol = 6*self.smearing
        if bin_size is None and bin_number is None:
            raise ValueError('At least one of `bin_size` or `bin_numbers '
                             'must be not None and larger than zero')
        if bin_number is not None:
            if bin_number > 0:
                self.bin_number = bin_number
                bin_size = (r_max + self.tol)/bin_number
                self.bin_size = bin_size
            elif bin_number <= 0:
                raise ValueError('`bin_number` must be greater than zero')
        elif bin_size > 0:
            bin_number = ceil((r_max + self.tol)/bin_size)
            self.bin_number = bin_number
            self.bin_size = bin_size
        else:
            raise ValueError('`bin_size` must be greater than zero')
        self._atomic_types, self._atomic_counts = np.unique(
            structure.get_atomic_numbers(), return_counts=True)
        self._atoms_by_type = self._divide_atoms_by_type(structure)
        self._extended_atoms, self._translations = self._get_extended_cell()
        self._atoms_by_type_ext = self._divide_atoms_by_type(
            self._extended_atoms)
        self._translations = np.ascontiguousarray(self._translations,
                                                  dtype=DTYPE)
        self.distance_table = self._calculate_distance_table()
        self.stoichiometry = self._get_compound_stoichiometry()
        self.pure_c = pure_c

    def _get_compound_stoichiometry(self):
        stoichiometry = {key: value
                         for (key, value)
                         in zip(self._atomic_types, self._atomic_counts)}
        return stoichiometry

    def _get_extended_cell(self):
        """ Find the extended cell such that all atoms within the maximum distance
         max(d_i) are included. Where d_i is one of the diagonals of the cell"""
        diags = self._find_length_cell_diagonals()
        dmax = np.max(np.array(diags))
        dmax = np.max([dmax, self.r_max])
        supercell_indices = []
        no_atoms = len(self._atoms)
        a, b, c, alp, bet, gam = self._atoms.get_cell_lengths_and_angles()
        no_cells = 1
        for param in [a, b, c]:
            arg = ceil(dmax/param) + 1
            supercell_indices.append(arg)
            no_cells *= (2*arg + 1)
        limits = [range(-x, x + 1) for x in supercell_indices]
        new_numbers = np.tile(self._atoms.get_atomic_numbers(), no_cells)
        new_scaled_positions = np.tile(self._atoms.get_scaled_positions(),
                                       (no_cells, 1))
        translations = np.zeros((no_cells, 3))
        index = 0
        for i1, p1 in enumerate(limits[0]):
            t1 = np.array([p1, 0, 0])
            for i2, p2 in enumerate(limits[1]):
                t2 = np.array([0, p2, 0])
                for i3, p3 in enumerate(limits[2]):
                    t3 = np.array([0, 0, p3])
                    t = t1 + t2 + t3
                    translations[index] = t
                    start = index*no_atoms
                    end = start + no_atoms
                    new_scaled_positions[start:end] += t
                    index += 1
        new_atoms = ase.atoms.Atoms(numbers=new_numbers,
                                    scaled_positions=new_scaled_positions,
                                    cell=self._atoms.cell[:])
        translations = np.dot(translations, self._atoms.cell)
        return new_atoms, translations

    def _find_length_cell_diagonals(self):
        cell = self._atoms.cell[:].copy()
        diagonals = []
        pstart = [np.zeros(3), cell[0], cell[0] + cell[1], cell[1]]
        pend = [np.sum(cell, axis=0), cell[1] + cell[2], cell[2],
                cell[0] + cell[2]]
        for i in range(4):
            v = pend[i] - pstart[i]
            diagonals.append(np.linalg.norm(v))
        return diagonals

    def _divide_atoms_by_type(self, atoms):
        """ Group together atoms of the same type"""
        atomic_types = self._atomic_types
        all_atoms = atoms.get_atomic_numbers()
        atoms_by_type = dict()
        for number in atomic_types:
            atoms_by_type[number] = []
            for i, anumber in enumerate(all_atoms):
                if anumber == number:
                    atoms_by_type[number].append(i)
        return atoms_by_type

    def _calculate_distance_table(self):
        pos = self._atoms.positions
        pos_ext = self._extended_atoms.positions
        distance_table = cdist(pos, pos_ext, metric='euclidean')
        return distance_table

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def _calculate_radial_fingerprint_a_b(self, int a, int b):
        """ Calculate the radial fingerprint between atom type ``a``
        and ``b`` discretized over the ``self.bin_number`` bins"""
        atoms_a = self._atoms_by_type[a]
        atoms_b = self._atoms_by_type[b]
        atoms_a = np.array(atoms_a, dtype=np.uintc)
        atoms_b = np.array(atoms_b, dtype=np.uintc)
        positions_a = self._atoms.positions[atoms_a]
        positions_b = self._atoms.positions[atoms_b]
        positions_a = np.ascontiguousarray(positions_a, dtype=DTYPE)
        positions_b = np.ascontiguousarray(positions_b, dtype=DTYPE)
        cdef double [:, ::1] positions_a_view = positions_a
        cdef double [:, ::1] positions_b_view = positions_b
        cdef Py_ssize_t ia, ib
        cdef unsigned int N_a = len(atoms_a)
        cdef unsigned int N_b = len(atoms_b)
        cdef double m_pi = np.pi
        cdef double [:, ::1] translations_view = self._translations
        cdef unsigned int N_cells = len(self._translations)
        cdef Py_ssize_t ni = 0

        cdef double tol = self.tol
        cdef double s2 = sqrt(2)*self.smearing
        cdef double bin_size = self.bin_size
        cdef double rab
        cdef unsigned int bin_min
        cdef unsigned int bin_max
        cdef double arg_min
        cdef double arg_min_i
        cdef double arg_max_i
        cdef unsigned int bin_no
        cdef unsigned int i = 0
        cdef unsigned int no_bins = 0
        cdef double value = 0
        cdef double vol = self._atoms.get_volume()
        cdef double norm = 4*m_pi*N_a*N_b*bin_size/vol
        cdef double r_max = self.r_max
        cdef double [::1] tmp = np.zeros(3, dtype=DTYPE, order='C')
        fingerprint = np.zeros(self.bin_number, dtype=DTYPE, order='C')
        cdef double [::1] fingerprint_view = fingerprint

        for ia in range(N_a):
            for ib in range(N_b):
                for ni in range(N_cells):
                    _add_positions(positions_b_view[ib],
                                   translations_view[ni],
                                   tmp, 3)
                    rab = _calculate_distance(tmp, positions_a_view[ia], 3)
                    if (rab < 1e-9) or (rab > r_max):
                        continue
                    # bins spanned by this gaussian
                    bin_min = <unsigned int> floor((rab - tol)/bin_size)
                    bin_max = <unsigned int> floor((rab + tol)/bin_size)
                    no_bins = bin_max + 1 - bin_min
                    arg_min = bin_min*bin_size
                    for i in range(no_bins):
                        bin_no = bin_min + i
                        arg_min_i = arg_min + i*bin_size
                        arg_max_i = arg_min_i + bin_size
                        arg_min_i -= rab
                        arg_max_i -= rab
                        value = 0.5*(erf(arg_max_i/s2) - erf(arg_min_i/s2))
                        value = value/rab/rab
                        fingerprint_view[bin_no] += value

        cdef Py_ssize_t endf = self.bin_number
        for i in range(endf):
            fingerprint_view[i] = fingerprint_view[i]/norm - bin_size

        return fingerprint

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def _calculate_radial_fingerprint_gradient_a_b(self, int a, int b):
        """ Calculates the gradient of F_AB with respect
        to all atoms in the unitcell
        """
        fingerprint_grad = np.zeros((3*len(self._atoms),
                                     self.bin_number), dtype=DTYPE, order='C')
        cdef double [:, ::1] fingerprint_grad_view = fingerprint_grad
        atoms_a = self._atoms_by_type[a]
        atoms_b = self._atoms_by_type[b]
        atoms_a = np.array(atoms_a, dtype=np.uintc)
        atoms_b = np.array(atoms_b, dtype=np.uintc)
        positions_a = self._atoms.positions[atoms_a]
        positions_b = self._atoms.positions[atoms_b]
        positions_a = np.ascontiguousarray(positions_a, dtype=DTYPE)
        positions_b = np.ascontiguousarray(positions_b, dtype=DTYPE)
        cdef double [:, ::1] positions_a_view = positions_a
        cdef double [:, ::1] positions_b_view = positions_b
        cdef unsigned int [::1] atoms_a_view = atoms_a
        cdef unsigned int [::1] atoms_b_view = atoms_b
        cdef int N_a = len(atoms_a)
        cdef int N_b = len(atoms_b)
        cdef Py_ssize_t ia, ib
        cdef double m_pi = np.pi

        cdef double [:, ::1] translations_view = self._translations
        cdef Py_ssize_t N_cells = self._translations.shape[0]
        cdef double tol = self.tol
        cdef double s2 = sqrt(2)*self.smearing
        cdef double pdiv = s2*sqrt(m_pi)
        cdef Py_ssize_t ni, i, j
        cdef double bin_size = self.bin_size
        cdef double rab, rab3
        cdef double r_max = self.r_max
        cdef double [::1] tmp = np.zeros(3, dtype=DTYPE, order='C')
        cdef double [::1] v_ab = np.zeros(3, dtype=DTYPE, order='C')
        cdef long bin_no
        cdef long bin_min, bin_max, no_bins
        cdef double arg_min, arg_min_i, arg_max_i
        cdef double value1, value2, totval
        cdef double vol = self._atoms.get_volume()
        cdef double norm = 4*m_pi*N_a*N_b*bin_size/vol

        for ia in range(N_a):
            for ib in range(N_b):
                for ni in range(N_cells):
                    _add_positions(positions_b_view[ib],
                                   translations_view[ni], tmp, 3)
                    rab = _calculate_distance(tmp,
                                              positions_a_view[ia], 3)
                    rab3 = pow(rab, 3)
                    if (rab < 1e-9) or (rab > r_max):
                        continue
                    _subtract_positions(tmp, positions_a_view[ia],
                                        v_ab, 3)
                    # bins spanned by this gaussian
                    bin_min = <int> floor((rab - tol)/bin_size)
                    bin_max = <int> floor((rab + tol)/bin_size)
                    no_bins = bin_max + 1 - bin_min
                    arg_min = bin_min*bin_size
                    for i in range(no_bins):
                        bin_no = bin_min + i
                        arg_min_i = arg_min + i*bin_size
                        arg_max_i = arg_min_i + bin_size
                        arg_min_i -= rab
                        arg_max_i -= rab
                        arg_min_i /= s2
                        arg_max_i /= s2
                        value1 = erf(arg_max_i) - erf(arg_min_i)
                        value1 /= rab
                        value2 = exp(-pow(arg_max_i, 2)) \
                            - exp(-pow(arg_min_i, 2))
                        value2 /= pdiv
                        totval = (value1 + value2)/rab3
                        for j in range(3):
                            fingerprint_grad_view[3*atoms_a_view[ia] + j,
                                                  bin_no] += \
                                totval*v_ab[j]/norm
                            fingerprint_grad_view[3*atoms_b_view[ib] + j,
                                                  bin_no] += \
                                -totval*v_ab[j]/norm

        return fingerprint_grad

    def _calculate_radial_fingerprint_a_b_pure_c(self, int a, int b):
        atoms_a = self._atoms_by_type[a]
        atoms_b = self._atoms_by_type[b]
        positions_a = self._atoms.positions[atoms_a]
        positions_b = self._atoms.positions[atoms_b]
        cdef double [:, ::1] positions_a_view = positions_a
        cdef double [:, ::1] positions_b_view = positions_b
        cdef double [:, ::1] translations_view = self._translations
        cdef size_t N_a = len(atoms_a)
        cdef size_t N_b = len(atoms_b)
        cdef size_t N_cells = len(self._translations)
        cdef double **positions_a_arr = allocate_memory_2d_array(N_a, 3)
        cdef double **positions_b_arr = allocate_memory_2d_array(N_b, 3)
        cdef double **translations_arr = allocate_memory_2d_array(N_cells, 3)
        cdef double tol = self.tol
        cdef double smearing = self.smearing
        cdef double bin_size = self.bin_size
        cdef double r_max = self.r_max
        cdef double volume = self._atoms.get_volume()
        cdef size_t bin_number = self.bin_number
        cdef double *fingerprint_a_b = <double *> malloc(bin_number*sizeof(double))
        if fingerprint_a_b is NULL:
            raise MemoryError()

        cdef size_t i
        cdef size_t j
        for i in range(bin_number):
            fingerprint_a_b[i] = 0.0

        for i in range(N_a):
            for j in range(3):
                positions_a_arr[i][j] = positions_a_view[i, j]
        for i in range(N_b):
            for j in range(3):
                positions_b_arr[i][j] = positions_b_view[i, j]
        for i in range(N_cells):
            for j in range(3):
                translations_arr[i][j] = translations_view[i, j]

        calculate_radial_fingerprints_a_b(positions_a_arr, positions_b_arr,
                                          translations_arr, N_a, N_b, N_cells,
                                          tol, smearing, bin_size, volume,
                                          r_max, fingerprint_a_b, bin_number)
        result = np.empty(bin_number, dtype=DTYPE)
        for i in range(bin_number):
            result[i] = fingerprint_a_b[i]
        free_memory_2d_array(positions_a_arr, N_a)
        free_memory_2d_array(positions_b_arr, N_b)
        free_memory_2d_array(translations_arr, N_cells)
        free(fingerprint_a_b)

        return result
    
    def _calculate_radial_fingerprint_gradient_a_b_pure_c(self, int a, int b):
        atoms_a = self._atoms_by_type[a]
        atoms_b = self._atoms_by_type[b]
        positions_a = self._atoms.positions[atoms_a]
        positions_b = self._atoms.positions[atoms_b]
        cdef double [:, ::1] positions_a_view = positions_a
        cdef double [:, ::1] positions_b_view = positions_b
        cdef double [:, ::1] translations_view = self._translations
        cdef unsigned int [::1] atoms_a_view = atoms_a
        cdef unsigned int [::1] atoms_b_view = atoms_b
        cdef size_t N_a = len(atoms_a)
        cdef size_t N_b = len(atoms_b)
        cdef size_t N_cells = len(self._translations)
        cdef size_t nat_a = len(atoms_a)
        cdef size_t nat_b = len(atoms_b)
        cdef double **positions_a_arr = allocate_memory_2d_array(N_a, 3)
        cdef double **positions_b_arr = allocate_memory_2d_array(N_b, 3)
        cdef double **translations_arr = allocate_memory_2d_array(N_cells, 3)
        cdef unsigned short *indices_a = <unsigned short *> malloc(nat_a*sizeof(unsigned short))
        cdef unsigned short *indices_b = <unsigned short *> malloc(nat_b*sizeof(unsigned short))
        if (indices_a is NULL) or (indices_b is NULL):
            raise MemoryError()
        cdef double tol = self.tol
        cdef double smearing = self.smearing
        cdef double bin_size = self.bin_size
        cdef double r_max = self.r_max
        cdef double volume = self._atoms.get_volume()
        cdef size_t bin_number = self.bin_number
        cdef size_t n_rows = 3*len(self._atoms)
        cdef double **fingerprint_grad_a_b = allocate_memory_2d_array(n_rows,
                                                                      bin_number)
        zero_2d_array(fingerprint_grad_a_b, n_rows, bin_number)

        cdef size_t i
        cdef size_t j
        for i in range(nat_a):
            indices_a[i] = atoms_a_view[i]
        for i in range(nat_b):
            indices_b[i] = atoms_b_view[i]
        for i in range(N_a):
            for j in range(3):
                positions_a_arr[i][j] = positions_a_view[i, j]
        for i in range(N_b):
            for j in range(3):
                positions_b_arr[i][j] = positions_b_view[i, j]
        for i in range(N_cells):
            for j in range(3):
                translations_arr[i][j] = translations_view[i, j]
        calculate_radial_fingerprint_gradient_a_b(positions_a_arr, positions_b_arr,
                                                  indices_a, indices_b,
                                                  translations_arr,
                                                  N_a, N_b, N_cells, tol,
                                                  smearing, bin_size, volume,
                                                  r_max, fingerprint_grad_a_b,
                                                  n_rows, bin_number)
        result = np.empty((n_rows, bin_number), dtype=DTYPE)
        for i in range(n_rows):
            for j in range(bin_number):
                result[i, j] = fingerprint_grad_a_b[i][j]
        free_memory_2d_array(positions_a_arr, N_a)
        free_memory_2d_array(positions_b_arr, N_b)
        free_memory_2d_array(translations_arr, N_cells)
        free_memory_2d_array(fingerprint_grad_a_b, n_rows)
        free(indices_a)
        free(indices_b)

        return result

    def calculate_radial_fingerprints(self):
        """ Calculate the radial fingerprint as a concatenation of pair
         fingerprints ordered by atomic number.
        """
        fingerprint = []
        atomic_types = list(self._atoms_by_type.keys())
        combinations = combinations_with_replacement(atomic_types, 2)
        if self.pure_c:
            getthem = self._calculate_radial_fingerprint_a_b_pure_c
        else:
            getthem = self._calculate_radial_fingerprint_a_b
        for atoma, atomb in combinations:
            fingerprint.append(getthem(atoma, atomb))
        fingerprint = np.concatenate(fingerprint)
        return fingerprint

    def calculate_radial_fingerprints_gradients(self):
        """ Calculate the radial fingerprint gradient as a concatenation
         of the gradients of pair fingerprints ordered by atomic number.
        """
        fingerprint_gradients = []
        atomic_types = list(self._atoms_by_type.keys())
        combinations = combinations_with_replacement(atomic_types, 2)
        if self.pure_c:
            getthem = self._calculate_radial_fingerprint_gradient_a_b_pure_c
        else:
            getthem = self._calculate_radial_fingerprint_gradient_a_b
        for atoma, atomb in combinations:
            grads_a_b = getthem(atoma, atomb)
            fingerprint_gradients.append(grads_a_b)
        return np.concatenate(fingerprint_gradients, axis=1)

    def get_descriptors(self):
        return self.calculate_radial_fingerprints()

    def get_descriptors_gradients(self):
        return self.calculate_radial_fingerprints_gradients()
