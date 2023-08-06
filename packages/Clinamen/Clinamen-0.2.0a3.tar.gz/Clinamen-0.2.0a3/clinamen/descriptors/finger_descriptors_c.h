/* Copyright 2020 Marco Arrigoni

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. */
#ifndef DESCRIPTORS_C_H
#define DESCRIPTORS_C_H

#include <stdlib.h>

// create fingerprint_a_b, a vector with bin_number elements
void calculate_radial_fingerprints_a_b(double **positions_a, double **positions_b,
                                       double **translations, size_t na, size_t nb,
                                       size_t nt, double tol, double smearing, double bin_size,
                                       double volume, double r_max, double *fingerprint_a_b,
                                       size_t bin_number);

// createt fingerprint_grad_a_b a 2D matrix with dofs rows and bin_number columns
void calculate_radial_fingerprint_gradient_a_b(double **positions_a, double **positions_b,
                                               unsigned short *indices_a, unsigned short *indices_b,
                                               double **translations, size_t na, size_t nb,
                                               size_t nt, double tol, double smearing, double bin_size,
                                               double volume, double r_max, double **fingerprint_grad_a_b,
                                               size_t dofs, size_t bin_number);

#endif /* DESCRIPTORS_C_H */
