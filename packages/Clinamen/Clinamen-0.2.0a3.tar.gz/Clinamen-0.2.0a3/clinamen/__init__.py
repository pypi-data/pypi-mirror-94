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

r""" Clinamen: Covariance-matrix-adaptation evolution strategy for Localized
Impurities with unsupervised Machine learning exploration of Non-elementary
structures.

**Clinamen** is a Python package implementing the covariance-matrix-adaptaion
evolution strategy (CMA-ES) for finding low-energy configurations of localized
defects. It additionally employs an unsupervised machine learning (ML) approach
for exploiting the structures visited by the evolutionary algorithm (EA) in order
to find additional low-energy minima.
"""
import numpy as np

from clinamen.__about__ import *

DESCRIPTORS_FLOAT_DTYPE = np.float32
INDIVIDUALS_FLOAT_DTYPE = np.float64
