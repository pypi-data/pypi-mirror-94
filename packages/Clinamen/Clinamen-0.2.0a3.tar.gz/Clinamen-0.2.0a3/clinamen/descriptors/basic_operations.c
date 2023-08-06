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
#include "basic_operations.h"

extern inline void add_vectors(double *v1, double *v2, double *res, size_t n);
extern inline void subtract_vectors(double *v1, double *v2, double *res, size_t n);
extern inline double calculate_vector_distance(double *v1, double *v2, size_t n);
