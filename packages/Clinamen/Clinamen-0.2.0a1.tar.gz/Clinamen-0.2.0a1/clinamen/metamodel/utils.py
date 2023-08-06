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
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.utils.validation import check_is_fitted, FLOAT_DTYPES


def _check_length_scale(length_scale):
    """ We consider only isotropic length scales"""
    length = np.squeeze(length_scale)
    if np.ndim(length) != 0:
        raise ValueError('Only isotropic length steps are accepted')
    return length


def _check_has_gradient(kernel):
    names = ['dKdX1', 'dKdX2', 'hessian', 'hessian_diagonal']
    for name in names:
        if not hasattr(kernel, name):
            raise TypeError('Can add only kernels with implemented gradients')


class StandardScalerGrad(StandardScaler):
    """ Scale inputs and outputs derivatives as appropriate"""
    def transform(self, X, dy=None, copy=None):
        """ Perform standardization by centering and scaling.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            the data to be scaled

        dy : array-like of shape (n_samples, n_features) or None. Default None
            if not None, represents the output derivatives data that
            should be scaled

        copy: bool. Default None
            copy the input X or not

        Returns
        -------
        X_tr : array-like, shape (n_samples, n_features)
             Transformed array.

        dy_tr : if dy is not None, array-like, shape (n_samples, n_features)
             Transformed array.
        """
        if dy is None:
            return super().transform(X, copy)

        check_is_fitted(self)
        copy = copy if copy is not None else self.copy
        X_params = {'copy': copy, 'estimator': self,
                    'dtype': FLOAT_DTYPES,
                    'force_all_finite': 'allow-nan'}
        y_params = {'copy': copy, 'estimator': self,
                    'dtype': FLOAT_DTYPES,
                    'force_all_finite': 'allow-nan'}
        X, dy = self._validate_data(X, dy,
                                    validate_separately=(X_params,
                                                         y_params))
        if self.with_mean:
            X -= self.mean_
        if self.with_std:
            X /= self.scale_
            dy *= self.scale_
        return X, dy

    def inverse_transform(self, X=None, dy=None, copy=None):
        """ Perform standardization by centering and scaling.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features). Default None
            the data to be scaled

        dy : array-like of shape (n_samples, n_features) or None. Default None
            if not None, represents the output derivatives data that
            should be scaled

        copy: bool. Default None
            copy the input X or not

        Returns
        -------
        X_tr : array-like, shape (n_samples, n_features)
            Transformed array.

        dy_tr : if dy is not None, array-like, shape (n_samples, n_features)
             Transformed array.
        """
        if X is None and dy is None:
            raise ValueError('At least one of X or dy must be not None')

        if dy is None:
            return super().inverse_transform(X, copy)

        check_is_fitted(self)
        copy = copy if copy is not None else self.copy

        if X is not None:
            X = np.asarray(X)
        dy = np.asarray(dy)
        if copy:
            if X is not None:
                X = X.copy()
            dy = dy.copy()
        if self.with_std:
            if X is not None:
                X *= self.scale_
            dy /= self.scale_
        if self.with_mean:
            if X is not None:
                X += self.mean_
        if X is None:
            return dy
        return X, dy

