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
import torch
import gpytorch


class ExactGPModel(gpytorch.models.ExactGP):
    """ GP model for exact inference """
    def __init__(self, train_x, train_y, mean_function, kernel_function,
                 likelihood, scale_kernel_kwargs=dict()):
        super(ExactGPModel, self).__init__(train_x, train_y, likelihood)
        self.mean_module = mean_function
        self.covar_module = gpytorch.kernels.ScaleKernel(kernel_function,
                                                         **scale_kernel_kwargs)

    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return gpytorch.distributions.MultivariateNormal(mean_x, covar_x)

