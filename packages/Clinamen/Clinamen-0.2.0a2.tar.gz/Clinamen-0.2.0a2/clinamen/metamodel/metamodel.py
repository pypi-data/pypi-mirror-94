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
from abc import ABC, abstractmethod
import copy
import numpy as np
from scipy.linalg import lstsq
from mpi4py import MPI

import torch
import gpytorch

from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from clinamen.utils import get_structure_id
from clinamen.evpd import ROOT_LOGGER as logger
from .gp_models import ExactGPModel


comm = MPI.COMM_WORLD
proc_no = comm.Get_rank()


class GPMetaModel(ABC):
    """ Class for creating a Gaussian Process metamodel.
    """
    def __init__(self, descriptors_database, 
                 mean_function=None, mean_function_kwargs=None,
                 kernel_function=None, kernel_function_kwargs=None,
                 likelihood_function=None, likelihood_function_kwargs=None,
                 optimizer=None, optimizer_kwargs=None,
                 marginal_likelihood_function=None,
                 marginal_likelihood_function_kwargs=None,
                 preprocessing_pipeline=None, std_value=1e-2):
        """
        Parameters
        ----------
        descriptors_database : object
            Instance of ``DescriptorsDatabase`` class used to produce
            some descriptors.

        mean_function : ``gpytorch.means`` class
            the class that once initialized produces the mean function.
            For example: ``mean_function=gpytorch.means.LinearMean``

        mean_function_kwargs : dict
            the parameters to instantiate the ``mean_function`` class.
            For example: ``mean_function_kwargs={'bias': False}``.
            The actual mean function to be used in the GP model will
            then be the object ``mean_function(**mean_function_kwargs)``

        kernel_function : ``gpytorch.kernels`` class
            the class that once initialized produces the kernel function

        kernel_function_kwargs : dict
            the parameters to instantiate the ``kernel_function`` class

        likelihood_function : ``gpytorch.likelihoods`` class
            the class that once initialized produces the likelihood function

        likelihood_function_kwargs : dict
            the parameters to instantiate the ``likelihood_function`` class

        optimizer : ``torch.optim`` class
            the class that once initialized produces the optimizer for
            maximizing the marginal likelihood

        optimizer_kwargs : dict
           the parameters for initializing the optimizer

        marginal_likelihood_function : ``gpytorch.mlls`` class
            the marginal likelihood class to be maximized

        marginal_likelihood_function_kwargs : dict
            the parameters for initializing the 
            ``marginal_likelihood_function``

        preprocessing_pipeline : ``sklearn.pipeline.Pipeline`` object
            A pipeline to preprocess the inputs data. The metamodel
            is trained using the inputs outputted by this pipeline.
            The trasformation of ``inputs`` must be accomplished by
            calling ``preprocessing_pipeline.fit_transform(``inputs``)``

        std_value : float. Default 1e-2 eV/atom
            when the prediction standard deviation is smaller than
            ``std_value``, the fitness for the individual will be taken
            from the surrogate model. Otherwise, they will be calculated
        """
        self.descriptors_database = descriptors_database
        self._mean_class = mean_function
        self._mean_kwargs = mean_function_kwargs
        self._kernel_class = kernel_function
        self._kernel_kwargs = kernel_function_kwargs
        self._likelihood_class = likelihood_function
        self._likelihood_kwargs = likelihood_function_kwargs
        self._optimizer_class = optimizer
        self._optimizer_kwargs = optimizer_kwargs
        self._mll_class = marginal_likelihood_function
        self._mll_kwargs = marginal_likelihood_function_kwargs
        self.preprocessing_pipeline = preprocessing_pipeline
        self.std_value = std_value

        self.train = True  # If True, we are in training mode
        self._loaded_state = False

    @abstractmethod
    def initialize_model(self, X_train, y_train):
        """ This function initializes the GP model (``gpytorch.models``)
        class, which means it initializes the mean function, kernel function,
        and the likelihood. The function also initializes the optimizer
        and the marginal log likelihood.

        All these initialized objects must be assigned
        to the respectie attributes:

        - ``self._mean_function``
        - ``self._kernel_function``
        - ``self._likelihood``
        - ``self._model``
        - ``self._optimizer``
        - ``self._mll``

        which can then be accessed through the corresponding property
        """

    @property
    def mean_function(self):
        return self._mean_function

    @property
    def kernel_function(self):
        return self._kernel_function

    @property
    def likelihood(self):
        return self._likelihood

    @property
    def model(self):
        return self._model

    @property
    def optimizer(self):
        return self._optimizer

    @property
    def mll(self):
        return self._mll

    @property
    def loaded_state(self):
        """ If True, it means that the state of the model has been
        loaded from an external file
        """
        return self._loaded_state

    def _write_and_retrieve_descriptors(self, structures):
        ### get the descriptors
        ids = [self.descriptors_database.get_structure_id(atom)
               for atom in structures]
        # we write and read from disk every time.
        self.descriptors_database.write_descriptors(structures) 
        descriptors, _ = self.descriptors_database.read_descriptors(ids)
        if proc_no == 0:
            logger.info(
                f'Obtained descriptors of shape {descriptors.shape}')
        ### pass the descriptors through the preprocessing pipeline
        if self.preprocessing_pipeline is None:
            X = descriptors
        else:
            if self.train:
                X = self.preprocessing_pipeline.fit_transform(descriptors)
            else:
                X = self.preprocessing_pipeline.transform(descriptors)
            if proc_no == 0:
                logger.info(
                    f'Transformed descriptors of shape {X.shape}')
        return X

    def fit(self, structures, y, epochs=10000, stopping=1e-3,
            stopping_epochs=10, verbose=False):
        """ Train the meta-model

        Parameters
        ----------
        population : Iterable of structures of length n_samples.

        y : ``np.ndarray`` of shape (n_samples, )
            the total energy of the structures in ``structures``

        epochs : int
            the number of epochs for training the metamodel

        stopping : float
            the loss function minimum change to trigger early stopping

        stopping_epochs : float
            for how many epochs the loss function should change by less than
            ``stopping`` in order to enforce early stopping

        verbose : bool
            If True, prints the loss function every 100 epochs
        """
        if proc_no == 0:
            logger.info(
                f'Training the metamodel with {len(structures)} structures')
        self.train = True
        X_train = self._write_and_retrieve_descriptors(structures)

        # to torch tensors
        X_train = torch.as_tensor(X_train, dtype=torch.float32)
        y = torch.as_tensor(y, dtype=torch.float32)

        ### Initialize all parts of the GP model
        self.initialize_model(X_train, y)

        ### train the metamodel
        self.model.train()
        self.likelihood.train()

        prev_loss_val = np.inf
        iter_stop = 0
        for i in range(epochs):
            self.optimizer.zero_grad()
            output = self.model(X_train)
            loss = -self.mll(output, y)
            loss.backward()
            loss_val = loss.detach().numpy()
            if i == 0:
                if proc_no == 0:
                    logger.info(f'Initial loss: {loss_val:.3f}')
            if verbose and i%100 == 0:
                if proc_no == 0:
                    logger.debug(f'Iter {i+1}/{epochs}.  '
                                 f'Loss = {loss_val:.3f}')
            self.optimizer.step()
            if np.abs(prev_loss_val - loss_val) < stopping:
                iter_stop += 1
                if iter_stop >= stopping_epochs:
                    if proc_no == 0:
                        logger.debug('Early stopping!')
                    break
            else:
                iter_stop = 0
            prev_loss_val = loss_val
        if proc_no == 0:
            logger.info(f'Model trained after {i+1} epochs. '
                        f'Final loss: {loss_val:.3f}')

    def predict(self, structures):
        """ Predict the total energy for each individuals in
        an iterable of structures.

        Parameters
        ----------
        population : Iterable of structures of length n_samples.

        Returns:
        --------
        mean : np.array
            the predicted energies

        std : np.array
            the predicted standard deviations
        """
        if proc_no == 0:
            logger.info(
                f'Making predictions with the metamodel for {len(structures)} '
                 'structures') 
        self.train = False
        X_test = self._write_and_retrieve_descriptors(structures)

        # to torch tensors
        X_test = torch.as_tensor(X_test, dtype=torch.float32)

        ### making predictions
        self.model.eval()
        self.likelihood.eval()

        with torch.no_grad(), gpytorch.settings.fast_pred_var():
            prediction_dist = self.likelihood(self.model(X_test))
            mean = prediction_dist.mean.detach().numpy()
            std = prediction_dist.stddev.detach().numpy()
        return mean, std

    def write_descriptors(self, structures):
        """ Save the descriptors into the database hdf5 file.
        """
        self.descriptors_database.write_descriptors(structures)

    def read_descriptors(self):
        """ Read the descriptors from the hdf5 database file.
        """
        descriptors, _ = self.descriptors_database.read_descriptors()
        return descriptors

    def save_model(self, filename='model_state.pth'):
        """ Save the GP model """
        torch.save(self.model.state_dict(), filename)

    def load_model_state(self, model_pth):
        self.state_dict = torch.load(model_pth)
        self._loaded_state = True


class ExactGPMetaModel(GPMetaModel):
    """ Class for making a meta-model based on a Gaussian Process
    Regressor with exact inference.
    """
    def initialize_model(self, X_train, y_train):
        self._mean_function = self._mean_class(**self._mean_kwargs)
        self._kernel_function = self._kernel_class(
            ard_num_dims=X_train.shape[-1], **self._kernel_kwargs)
        self._likelihood = self._likelihood_class(**self._likelihood_kwargs)
        self._model = ExactGPModel(X_train, y_train, self._mean_function,
                                   self._kernel_function, self._likelihood,
                                   scale_kernel_kwargs=dict())
        self._optimizer = self._optimizer_class(self._model.parameters(),
                                                **self._optimizer_kwargs)
        self._mll = self._mll_class(self._likelihood, self._model,
                                    **self._mll_kwargs)


class BaseExactGPMetaModel(ExactGPMetaModel):
    """ Basic Exact GP regressor with a RBF kernel for minimal initialization
    effort.
    """
    def __init__(self, descriptors_database,
                 preprocessing_pipeline=None, std_value=1e-2):
        """
        Parameters
        ----------
        descriptors_database : object
            Instance of ``DescriptorsDatabase`` class used to produce
            some descriptors.

        preprocessing_pipeline : ``sklearn.pipeline.Pipeline`` object
            A pipeline to preprocess the inputs data. The metamodel
            is trained using the inputs outputted by this pipeline.
            The trasformation of ``inputs`` must be accomplished by
            calling ``preprocessing_pipeline.fit_transform(``inputs``)``

        std_value : float. Default 1e-2 eV/atom
            when the prediction standard deviation is smaller than
            ``std_value``, the fitness for the individual will be taken
            from the surrogate model. Otherwise, they will be calculated
        """
        mean_func = gpytorch.means.ConstantMean
        kernel_func = gpytorch.kernels.RBFKernel
        likelihood = gpytorch.likelihoods.GaussianLikelihood
        noise_constraint = gpytorch.constraints.Interval(1e-5, 1e-1)
        likelihood_kwargs = dict(noise_covar=1e-3, noise_constraint=noise_constraint)
        optimizer = torch.optim.Adam
        optimizer_kwargs = dict(lr=1e-2, amsgrad=True)
        marginal_log_likelihood = gpytorch.mlls.ExactMarginalLogLikelihood

        super().__init__(descriptors_database, mean_func, dict(),
                         kernel_func, dict(), likelihood, likelihood_kwargs,
                         optimizer, optimizer_kwargs,
                         marginal_log_likelihood, dict(),
                         preprocessing_pipeline, std_value)


class BasePCAExactGPMetaModel(BaseExactGPMetaModel):
    """ Basic Exact GP regressor with a RBF kernel for minimal initialization
    effort. The inputs are automatically passed through a pipeline that scales
    them and then performs PCA
    """
    def __init__(self, descriptors_database,
                 scaler_kwargs, pca_kwargs,
                 std_value=1e-2):
        """
        Parameters
        ----------
        descriptors_database : object
            Instance of ``DescriptorsDatabase`` class used to produce
            some descriptors.

        scaler_kwargs : dict
            parameters to initialize a ``sklean`` ``StandardScaler`` object

        pca_kwargs : dict
            parameters to initialize a ``sklearn`` ``PCA`` object

        std_value : float. Default 1e-2 eV/atom
            when the prediction standard deviation is smaller than
            ``std_value``, the fitness for the individual will be taken
            from the surrogate model. Otherwise, they will be calculated
        """
        scaler = StandardScaler(**scaler_kwargs)
        pca = PCA(**pca_kwargs)
        steps = [
            ('scaler', scaler),
            ('pca', pca)
        ]
        pipeline = Pipeline(steps)
        super().__init__(descriptors_database, pipeline, std_value)
