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
#include <stdlib.h>
#include <math.h>
#include "basic_operations.h"

void calculate_radial_fingerprints_a_b(double **positions_a, double **positions_b,
                                       double **translations, size_t na, size_t nb,
                                       size_t nt, double tol, double smearing, double bin_size,
                                       double volume, double r_max, double *fingerprint_a_b,
                                       size_t bin_number) {
    double s2 = sqrt(2)*smearing;
    double rab;
    double arg_min, arg_min_i, arg_max_i;
    unsigned long bin_no, bin_min, bin_max, no_bins;
    double value;
    double tmp[3] = {0.};
    
    double norm = 4*M_PI*na*na*bin_size/volume;
    
    for (size_t j = 0; j < bin_number; j++)
        fingerprint_a_b[j] = 0;

    for (size_t ia = 0; ia < na; ia++) {
        for (size_t ib = 0; ib < nb; ib++) {
            for (size_t ni = 0; ni < nt; ni++) {
                add_vectors(positions_b[ib], translations[ni], tmp, 3);
                rab = calculate_vector_distance(tmp, positions_a[ia], 3);
                if ((rab < 1e-9) || (rab > r_max)) continue;
                
                bin_min = (unsigned long) floor((rab - tol)/bin_size); 
                bin_max = (unsigned long) floor((rab + tol)/bin_size); 
                no_bins = bin_max + 1 - bin_min;
                arg_min = bin_min*bin_size;
                for (unsigned long i = 0; i < no_bins; i++) {
                    bin_no = bin_min + i;
                    arg_min_i = arg_min + i*bin_size;
                    arg_max_i = arg_min_i + bin_size;
                    arg_min_i -= rab;
                    arg_max_i -= rab;
                    value = 0.5*(erf(arg_max_i/s2) - erf(arg_min_i/s2));
                    value = value/rab/rab;
                    fingerprint_a_b[bin_no] += value;
                }
            }
        }
    }

    for (size_t j = 0; j < bin_number; j++)
        fingerprint_a_b[j] = fingerprint_a_b[j]/norm - bin_size; 
}


void calculate_radial_fingerprint_gradient_a_b(double **positions_a, double **positions_b,
                                               unsigned short *indices_a, unsigned short *indices_b,
                                               double **translations, size_t na, size_t nb,
                                               size_t nt, double tol, double smearing, double bin_size,
                                               double volume, double r_max, double **fingerprint_grad_a_b,
                                               size_t dofs, size_t bin_number) {
    double s2 = sqrt(2)*smearing;
    double pdiv = s2*sqrt(M_PI);
    double rab, rab3;
    double arg_min, arg_min_i, arg_max_i;
    unsigned long bin_no, bin_min, bin_max, no_bins;
    double value1, value2, totval;
    double tmp[3] = {0.};
    double v_ab[3] = {0.};
    
    double norm = 4*M_PI*na*na*bin_size/volume;
    
    for (size_t j1 = 0; j1 < dofs; j1++) {
        for (size_t j2 = 0; j2 < bin_number; j2++) {
            fingerprint_grad_a_b[j1][j2] = 0;
        }
    }

    for (size_t ia = 0; ia < na; ia++) {
        for (size_t ib = 0; ib < nb; ib++) {
            for (size_t ni = 0; ni < nt; ni++) {
                add_vectors(positions_b[ib], translations[ni], tmp, 3);
                rab = calculate_vector_distance(tmp, positions_a[ia], 3);
                if ((rab < 1e-9) || (rab > r_max)) continue;
                
                rab3 = pow(rab, 3);
                subtract_vectors(tmp, positions_a[ia], v_ab, 3);
                bin_min = (unsigned long) floor((rab - tol)/bin_size); 
                bin_max = (unsigned long) floor((rab + tol)/bin_size); 
                no_bins = bin_max + 1 - bin_min;
                arg_min = bin_min*bin_size;
                for (unsigned long i = 0; i < no_bins; i++) {
                    bin_no = bin_min + i;
                    arg_min_i = arg_min + i*bin_size;
                    arg_max_i = arg_min_i + bin_size;
                    arg_min_i -= rab;
                    arg_max_i -= rab;
                    arg_min_i /= s2;
                    arg_max_i /= s2;
                    value1 = erf(arg_max_i) - erf(arg_min_i);
                    value1 /= rab;
                    value2 = exp(-pow(arg_max_i, 2)) - exp(-pow(arg_min_i, 2));
                    value2 /= pdiv;
                    totval = (value1 + value2)/rab3;
                    for (unsigned short j = 0; j < 3; j++) {
                        fingerprint_grad_a_b[3*indices_a[ia] + j][bin_no] += 
                             totval*v_ab[j]/norm;
                        fingerprint_grad_a_b[3*indices_b[ib] + j][bin_no] += 
                            -totval*v_ab[j]/norm;
                    }
                }
            }
        }
    }
}
