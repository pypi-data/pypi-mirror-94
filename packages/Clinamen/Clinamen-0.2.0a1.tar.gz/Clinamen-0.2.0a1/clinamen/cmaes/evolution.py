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
import math
import numpy as np
import os
import json

from clinamen.utils import GeneralizedEncoder


class StrategyParameters:
    """ Class for the initialization, update and tracking of
    the CMA-ES algorithm.

    Parameters
    ----------
    dimension : int
        dimensionality of the problem. 

    pop_size : int or None
        population size

    weights : tuple with ``pop_size`` entries or None
        weights used in the algorithm

    c_sigma : float in (0, 1) or None
        learning rate for the conjugate evolution path used
        for step-size control

    d_sigma : float > 0 or None
        damping term

    c_c : float in [0, 1] or None
        learning rate for the evolution path used in the
        cumulation procedure

    c_1 : float in [0, 1] or None
        learning rate for the rank-1 update of the covariance
        matrix

    c_mu : float in [0, 1] or None
        learning rate for the rank-mu update of the covariance
        matrix
        
    alpha_cov : float or None
        parameter for calculating default values of the learning
        rates

    c_m : float or None
        learning rate for updating the mean. Generally 1, usually <= 1

    std_min : float or None
        increase the global step size if the std of the individuals
        fitness is below this value

    c_g : float or None
        learning rate for the evolution path of the gradient
        It is used only when the CMAES instance supports gradient usage

    Notes
    -----
    If some parameters are ``None``, default values will be used.
    It is suggested to leave all the parameters to their default value,
    with the exception of ``pop_size`` and ``alpha_cov`` at most.
    """    
    def __init__(self, dimension, pop_size=None, weights=None,
                 c_sigma=None, d_sigma=None, c_c=None, c_1=None, c_mu=None,
                 alpha_cov=None, c_m=None, std_min=None, c_g=None):
        if dimension <= 0 or type(dimension) is not int:
            raise ValueError("'dimension' must be a positive integer")
        self.n = dimension

        if pop_size is None:
            self.pop_size = 4 + math.floor(3*math.log(dimension))
        else:
            if pop_size <= 0 or type(pop_size) is not int:
                raise ValueError("'pop_size' must be a positive integer")
            self.pop_size = pop_size

        if c_m is None:
            self.c_m = 1
        else:
            self.c_m = c_m

        if std_min is None:
            self.std_min = 1e-15
        else:
            self.std_min = std_min

        self.mu = math.floor(self.pop_size/2)
        self.weights_prime = self._get_preliminary_convex_shape()
        self.mu_eff = self._get_mu_eff()

        if c_sigma is None:
            self.c_sigma = self._default_c_sigma()
        else:
            if not (0 < c_sigma < 1):
                raise ValueError("'c_sigma' must be in (0, 1)")
            self.c_sigma = c_sigma

        if d_sigma is None:
            self.d_sigma = self._default_d_sigma()
        else:
            if d_sigma <= 0:
                raise ValueError("'d_sigma' must be greater than 0")
            self.d_sigma = d_sigma

        if c_c is None:
            self.c_c = self._default_c_c()
        else:
            if not (0 <= c_c <= 1):
                raise ValueError("'c_c' must be in [0, 1]")
            self.c_c = c_c

        if alpha_cov is None:
            self.alpha_cov = 2
        else:
            self.alpha_cov = alpha_cov

        if c_1 is None:
            self.c_1 = self._default_c_1()
        else:
            if not (0 <= c_1 <= 1):
                raise ValueError("'c_1' must be in [0, 1]")
            self.c_1 = c_1

        if c_mu is None:
            self.c_mu = self._default_c_mu()
        else:
            if not (0 <= c_mu <= 1):
                raise ValueError("'c_mu' must be in [0, 1]")
            self.c_mu = c_mu

        if weights is None:
            self.weights = self._default_weights()
        else:
            if not isinstance(weights, (tuple, list, np.ndarray)) or \
                              len(weights) != pop_size:
                raise ValueError("'weights' must be an array of length "
                                 "{}".format(self.pop_size))
            self.weights = weights

        if c_g is not None:
            if not (0 <= c_g <= 1):
                raise ValueError("'c_g' must be in [0, 1]")
        self.c_g = c_g

    def _get_preliminary_convex_shape(self):
        """ Return the preliminary weights """
        log_term = np.log(np.arange(1, self.pop_size + 1))
        preliminary_weights = np.log((self.pop_size + 1)/2) - log_term
        return preliminary_weights

    def _get_mu_eff(self):
        weights_prime = self.weights_prime
        num = np.sum(weights_prime[:self.mu])
        den = np.sum(weights_prime[:self.mu]**2)
        mu_eff = num*num/den
        return mu_eff

    def _get_mu_eff_minus(self):
        weights_prime = self.weights_prime
        num = np.sum(weights_prime[self.mu:])
        den = np.sum(weights_prime[self.mu:]**2)
        mu_eff = num*num/den
        return mu_eff

    def _get_alpha_mu_minus(self):
        return 1 + self.c_1/self.c_mu

    def _get_alpha_mu_eff_minus(self):
        mu_eff_minus = self._get_mu_eff_minus()
        return 1 + (2*mu_eff_minus/(self.mu_eff + 2))

    def _get_alpha_pos_def(self):
        return (1 - self.c_1 - self.c_mu)/self.n/self.c_mu

    def _default_weights(self):
        weights_prime = self.weights_prime
        sum_plus = np.sum(np.abs(weights_prime[:self.mu]))
        sum_minus = np.sum(np.abs(weights_prime[self.mu:]))
        weights = np.zeros(self.pop_size)
        weights[:self.mu] = weights_prime[:self.mu]/sum_plus
        m_factor = np.min([self._get_alpha_mu_minus(),
                           self._get_alpha_mu_eff_minus(),
                           self._get_alpha_pos_def()])
        weights[self.mu:] = weights_prime[self.mu:]*m_factor/sum_minus
        return weights

    def _default_c_sigma(self):
        return (self.mu_eff + 2)/(self.n + self.mu_eff + 5)

    def _default_d_sigma(self):
        term = np.sqrt((self.mu_eff - 1)/(self.n + 1)) - 1
        return 1 + 2*np.max([0, term]) + self.c_sigma

    def _default_c_c(self):
        num = 4 + self.mu_eff/self.n
        den = self.n + 4 + 2*self.mu_eff/self.n
        return num/den

    def _default_c_1(self):
        den = (self.n + 1.3)**2 + self.mu_eff
        return self.alpha_cov/den

    def _default_c_mu(self):
        term1 = 1 - self.c_1
        t2num = self.mu_eff - 2 + 1/self.mu_eff
        t2den = (self.n + 2)**2 + self.alpha_cov*self.mu_eff/2
        term2 = self.alpha_cov*t2num/t2den
        return np.min([term1, term2])

    def as_dict(self):
        """ Returns a dictionary with the parameters needed to initialize
        a ``StrategyParameters`` instance """
        params = dict()
        params['dimension'] = self.n
        params['pop_size'] = self.pop_size
        params['weights'] = self.weights.copy()
        params['c_sigma'] = self.c_sigma
        params['d_sigma'] = self.d_sigma
        params['c_c'] = self.c_c
        params['c_1'] = self.c_1
        params['c_mu'] = self.c_mu
        params['alpha_cov'] = self.alpha_cov
        params['c_m'] = self.c_m
        params['std_min'] = self.std_min
        return params


class TerminationConditionMet(Exception):
    pass


class TerminationCriteria:
    """ A class for holding the various termination criteria
    suggested for the algorithm. If a value is set to None/False,
    the corresponding criterium will be ingored.

    Parameters
    ----------
    noeffectaxis : bool

    noeffectcoord : bool

    conditioncov : bool

    equalfunvalues : bool

    maxiter : int
        maximum number of iterations

    tolxup : bool

    smallstd : float
        stop if the fitness std remains below ``smallstd`` for
        at least 15 iterations.
    """
    def __init__(self, noeffectaxis=True, noeffectcoord=True,
                 conditioncov=True, equalfunvalues=True, maxiter=1000,
                 tolxup=True, smallstd=1e-15):
        self.noeffectaxis = noeffectaxis
        self.noeffectcoord = noeffectcoord
        self.conditioncov = conditioncov
        self.equalfunvalues = equalfunvalues
        self.maxiter = maxiter
        self.tolxup = tolxup
        self.smallstd = smallstd
        
        self._smallstd_count = 0
        self._smallstd_max = 10  #int(0.1*maxiter)

        self._fitness_range = []
        self._D_hist = []
        self._attr = [attr for attr in self.__dict__.keys() 
                      if not attr.startswith('_')]
        self._tests = ['_test_' + x for x in self._attr]

    def set_params(self, cmaes):
        """ From an instance of a CMAES object, set the value of the
        needed parameters. """
        self._m = cmaes.m
        self._C = cmaes.C
        self._n = cmaes.dimension
        self._pop_size = cmaes.pop_size
        self._D = np.diag(np.sqrt(cmaes._D2))
        self._D_hist.append(np.max(self._D)*cmaes.step_size)
        self._g = cmaes.g
        self._step_size = cmaes.step_size
        self._B = cmaes._B

        self._cmaes = cmaes

    def _test_noeffectaxis(self):
        m = self._m
        index = self._g % self._n
        m_up = m + 0.1*self._step_size*self._D[index]*self._B[:, index]
        return np.allclose(m, m_up, rtol=0, atol=1e-16)

    def _test_noeffectcoord(self):
        cs = np.diag(self._C)
        step = self._step_size*0.2
        M = self._m + np.diag(cs)*step
        diff = np.sum(M - self._m, axis=1)
        return np.any(np.abs(diff) < 1e-16)

    def _test_conditioncov(self):
        tol = 1e14
        k = np.linalg.cond(self._C)
        return k >= tol

    def _test_equalfunvalues(self):
        self._fitness_range.append(np.max(self._cmaes._fitnesses) -
                                   np.min(self._cmaes._fitnesses))
        l_min = 10 + math.ceil(30*self._n/self._pop_size)
        l = len(self._fitness_range)
        if l < l_min:
            return False
        return np.all(self._fitness_range[l_min:] == 0)

    def _test_maxiter(self):
        return self._g >= self.maxiter

    def _test_tolxup(self):
        if len(self._D_hist) < 2:
            return False
        return self._D_hist[-1] - self._D_hist[0] > 1e4

    def _test_smallstd(self):
        fitnesses = self._cmaes._fitnesses
        std = np.std(fitnesses)
        if std <= self.smallstd:
            self._smallstd_count += 1
        else:
            self._smallstd_count = 0
        return self._smallstd_count == self._smallstd_max

    def terminate(self):
        message = 'Termination criterion "{}" met. Ending the loop'
        messages = ''
        test_vals = []
        for test, cond in zip(self._tests, self._attr):
            val = getattr(self, test)()
            if val:
                messages += message.format(cond) + '\n'
            test_vals.append(val)
        if np.any(test_vals):
            raise TerminationConditionMet(messages)

    def as_dict(self):
        """ Returns a dictionary with the parameters needed to initialize
        a ``TerminationCriteria`` instance """
        params = dict()
        params['noeffectaxis'] = self.noeffectaxis
        params['noeffectcoord'] = self.noeffectcoord
        params['conditioncov'] = self.conditioncov
        params['equalfunvalues'] = self.equalfunvalues
        params['maxiter'] = self.maxiter
        params['tolxup'] = self.tolxup
        params['smallstd'] = self.smallstd
        return params


class CMAES:
    """ Implementation of the covariance matrix adaptation
    evolution strategy.

    Parameters
    ----------
    strategy_params : StrategyParameters object
        contains the initial strategy parameters

    mean : 1D NumPy array
        the mean vector. If None, is taken as the zero vector

    covariance : 2D NumPy array
        the covariance matrix. If None, is taken as the identity matrix

    step_size : float
        the global variance. If None, is taken as 1

    random_seed : int
        the random seed for the random number generator

    terminator : TerminationCriteria instance
        object that keeps track of termination criteria.
        If None, a default one will be used.

    Notes
    -----
    If given, ``mean`` must have shape (``strategy_params.n``, ) and
    covariance (``strategy_params.n``, ``strategy_params.n``)
    """
    cmaes_parameters = ['mean', 'covariance', 'step_size',
                        'random_seed']

    def __init__(self, strategy_params, mean=None, covariance=None,
                 step_size=None, random_seed=10, terminator=None):
        self._random_seed = random_seed
        np.random.seed(random_seed)

        if not isinstance(strategy_params, StrategyParameters):
            raise TypeError("Must be an instance of 'StrategyParameters'")
        self._StrategyParameters = strategy_params
        self._dimension = self.StrategyParameters.n
        
        if mean is None:
            self._m = np.zeros(self.dimension)
        else:
            if mean.shape != (self.dimension, ):
                raise ValueError("The mean vector must have shape "
                                 "{} ".format((self.dimension, )))
            self._m = mean.copy()

        if covariance is None:
            self._C = np.eye(self.dimension)
        else:
            if covariance.shape != (self.dimension, self.dimension):
                raise ValueError(
                    "The covariance matrix must have "
                    "shape {} ".format((self.dimension, self.dimension)))
            self._C = covariance.copy()
        self._update_eigen_decomposition_C()
        self._update_C_sqrt_inv()

        if step_size is None:
            self._step_size = 1
        else:
            self._step_size = step_size
        self._step_size_0 = self._step_size

        # evolution paths
        self._p_sigma = np.zeros_like(self.m)
        self._p_c = np.zeros_like(self.m)

        self._g = 0    # generation index
     
        n = self.dimension
        # expected value norm of a standard normal random variable
        try:
            self._expected_norm_standard = math.sqrt(2)* \
                    math.gamma((n+1)/2)/math.gamma(n/2)
        except OverflowError:
            self._expected_norm_standard = math.sqrt(n)*(1 - 1/4/n + 1/21/n/n)

        if terminator:
            self._terminator = terminator
        else:
            self._terminator = TerminationCriteria()

    @property
    def StrategyParameters(self):
        """ The current instance of ``StrategyParameters`` """
        return self._StrategyParameters

    @property
    def Terminator(self):
        """ The current instance of ``TerminationCriteria``"""
        return self._terminator

    @property
    def random_seed(self):
        """ The user random seed"""
        return self._random_seed

    @property
    def dimension(self):
        return self._dimension

    @property
    def m(self):
        """ The mean vector for the current generation """
        return self._m

    @property
    def C(self):
        """ The covariance matrix for the current generation """
        return self._C

    @property
    def step_size(self):
        """ The step size for the current generation """
        return self._step_size

    @property
    def g(self):
        """ The index of the current generation """
        return self._g

    @property
    def pop_size(self):
        """ The population size """
        return self.StrategyParameters.pop_size

    @property
    def offspring(self):
        """ The offspring object parameters in the current generation """
        return self._offspring

    @property
    def mutated_offspring(self):
        """ The offpsring object parameters obtained after the mutation """
        return self._mutated_offspring

    def set_mutated_offspring(self, x):
        """ When manual mutation is selected, this method must be used to
        insert the mutated individuals

        Parameters
        ----------
        x : 2D NumPy array of shape (``self.pop_size``, ``self.dimension``)
            the object parameters of the mutated individuals
        """
        self._mutated_offspring = x.copy()

    def set_fitness_calculator(self, calculator):
        """ Set a fitness calculator: any object that can take object
        parameters representing the individuals (one row = one individual)
        and implements a method that calculates the fitness of individuals.

        Basic interface of this fitness calculator:

            - A method called ``set_object_parameters`` which accepts a
              2D NumPy array of shape (``self.pop_size``, ``self.dimension``)

            - A method called ``get_fitness`` that returns an array of shape
              (``self.pop_size``, ) with the calculated fitness for each
              individual

            - Eventally, a method called ``get_gradients`` that
              returns an array of shape
              (``self.pop_size``, ``self.dimension``) with the calculated
              gradients


        Parameters
        ----------
        calculator : a fitness calculator instance
        """
        methods = ['set_object_parameters', 'get_fitness']
        for method in methods:
            if not hasattr(calculator, method):
                raise AttributeError("The fitness calculator has no "
                                     "'{}' method".format(method))
        self._fitness_calculator = calculator

    def _set_ranked_individuals(self, x):
        """ Set the object parameters of the individuals
        in the current generation, ordered from highest to smallest
        fitness. This function exists in order to achieve high flexibility:
        the object calculating the fitness can be anything, it just needs
        to return the object parameters.

        Parameters
        ----------
        x_best : 2D NumPy array
            array of shape (``self.pop_size``, ``self.dimension``)
        """
        if not x.shape == (self.pop_size, self.dimension):
            raise ValueError("The shape of the array must be "
                             f"({self.pop_size, self.dimension}) "
                             f"got ({x.shape})")
        self._offspring = x.copy()
        self._centered_offspring = (self._offspring - self.m)/self.step_size

    def _update_eigen_decomposition_C(self):
        """ Computes eigendecomposition of the covariance matrix """
        eigvals, eigvecs = np.linalg.eigh(self._C)
        self._B = eigvecs
        self._D2 = np.diag(eigvals)
        self._BD = np.dot(self._B, np.sqrt(self._D2))

    def _update_C_sqrt_inv(self):
        """ Calculate the inverse of the square root of the
        covariance matrix """
        D = np.diag(np.sqrt(self._D2))
        D_inv = np.diag(1/D)
        C_sqrt_inv = np.dot(self._B, np.dot(D_inv, self._B.T))
        self._C_sqrt_inv = C_sqrt_inv

    def _mutate_single(self):
        """ Use in cases where one has to check for each individual
        whether the mutation gives a reasonable configuration.
        """
        size = self.dimension
        z = np.random.standard_normal(size=size)
        y = np.dot(self._BD, z)
        x = self.m + self.step_size*y
        return x

    def _mutate(self):
        """ Generate the offspring through mutation.
        These can be accessed from some object which will use them
        to calculate the fitnesses.
        """
        size = (self.pop_size, self.dimension)
        z = np.random.standard_normal(size=size)
        y = np.dot(z, self._BD.T)
        x = self.m + self.step_size*y

        self._mutated_offspring = x

    def _update_mean(self):
        self._m = (self._m
                   + self.StrategyParameters.c_m*self.step_size*self._yw)

    def _select_and_recombine(self):
        mu = self.StrategyParameters.mu
        try:
            offspring = self._offspring
        except AttributeError:
            raise AttributeError("Ranked individuals missing for "
                                 "generation {}, use "
                                 "'_set_ranked_individuals'".format(self.g))
        centered_offspring = self._centered_offspring
        weights = self.StrategyParameters.weights
        arg = weights[:, np.newaxis]*centered_offspring
        yw = np.sum(arg[:mu], axis=0)
        self._yw = yw
        self._update_mean()

    def _step_size_control(self):
        c_sigma = self.StrategyParameters.c_sigma
        d_sigma = self.StrategyParameters.d_sigma
        mu_eff = self.StrategyParameters.mu_eff
        pref1 = 1 - c_sigma
        pref2 = np.sqrt(c_sigma*(2 - c_sigma)*mu_eff)
        yw_white = np.dot(self._C_sqrt_inv, self._yw)
        self._p_sigma = pref1*self._p_sigma + pref2*yw_white
        nn = self._expected_norm_standard
        term = np.linalg.norm(self._p_sigma)/nn - 1
        self._step_size *= math.exp(c_sigma*term/d_sigma)

    def _covariance_matrix_adaptation(self):
        c_sigma = self.StrategyParameters.c_sigma
        c_c = self.StrategyParameters.c_c
        c_1 = self.StrategyParameters.c_1
        c_mu = self.StrategyParameters.c_mu
        mu_eff = self.StrategyParameters.mu_eff
        comp_term = np.linalg.norm(self._p_sigma)/math.sqrt(1 - 
                                   (1 - c_sigma)**(2*(self.g + 1)))
        comp_val = (1.4 + 2/(self.dimension + 1))*self._expected_norm_standard
        if comp_term < comp_val:
            h_sigma = 1
        else:
            h_sigma = 0
        pref1 = 1 - c_c
        pref2 = h_sigma*math.sqrt(c_c*(2 - c_c)*mu_eff)
        self._p_c = pref1*self._p_c + pref2*self._yw

        mu = self.StrategyParameters.mu
        weights = self.StrategyParameters.weights
        weights_circ = weights.copy()
        y_worst = self._centered_offspring[mu:]
        term = np.dot(y_worst, self._C_sqrt_inv.T)
        term = np.linalg.norm(term, axis=1)**2
        weights_circ[mu:] *= self.dimension/term
        delta_h_sigma = (1 - h_sigma)*c_c*(2 - c_c)
        pref1 = 1 + c_1*delta_h_sigma - c_1 - c_mu*np.sum(weights)
        term1 = c_1*np.outer(self._p_c, self._p_c)
        Y = weights_circ[:, np.newaxis]*self._centered_offspring
        Y_p = self._centered_offspring
        term2 = np.dot(Y.T, Y_p)
        term2 *= c_mu
        self._rank_1_C = term1
        self._rank_mu_C = term2
        self._C = pref1*self._C + term1 + term2

    def _next_generation(self, **kwargs):
        """ Evolve the population to the next generation """
        try:
            calculator = self._fitness_calculator
        except AttributeError:
            raise AttributeError("A fitness calculator is mandatory. "
                                 "Use 'set_fitness_calculator'")

        manual_mutation = kwargs.get('manual_mutation', False)

        if not manual_mutation:
            self._mutate()
        self._g += 1
        x = self.mutated_offspring
        calculator.set_object_parameters(x)
        fitnesses = calculator.get_fitness()
        self._fitnesses = fitnesses.copy()
        sorted_ind = np.argsort(-fitnesses)
        x_ranked = x[sorted_ind]
        self._set_ranked_individuals(x_ranked)
        self._select_and_recombine()
        self._step_size_control()
        if np.std(fitnesses) <= self.StrategyParameters.std_min:
            c_sigma = self.StrategyParameters.c_sigma
            d_sigma = self.StrategyParameters.d_sigma
            self._step_size *= np.exp(1 + c_sigma/d_sigma)
        self._covariance_matrix_adaptation()
        self._update_eigen_decomposition_C()
        self._update_C_sqrt_inv()

        self._terminator.set_params(self)

        current_params = {'g': self.g, 'C': self.C.copy(),
                          'fitnesses': self._fitnesses.copy(),
                          'chromosomes': self.offspring.copy(),
                          'step_size': self.step_size,
                          'mean': self.m.copy()}
        return current_params

    def evolve(self, manual_mutation=False):
        """ Generator for the evolutionary process.

        Parameters
        ----------
        manual_mutation : bool
            When True, mutated individuals must be inserted manually using
            the method ``set_mutated_offspring``

        Yield
        -----
        a dictionary with the relevant parameters for the current generation
        """
        while True:
            yield self._next_generation(manual_mutation=manual_mutation)
            try:
                self._terminator.terminate()
            except TerminationConditionMet as e:
                print('Termination ended due to:\n\t' + str(e))
                break

    def _prepare_json_data(self):
        data = dict()
        data['cmaes'] = self.as_dict()
        sparams = self.StrategyParameters
        data['StrategyParameters'] = sparams.as_dict()
        tparams = self._terminator
        data['TerminationCriteria'] = tparams.as_dict()
        return data

    def save_status(self, path=None):
        """ Save a json file with the data representing the current status
        of the evolution. Only data needed to restart a CMAES object are
        saved.

        Parameters
        ----------
        path : str or None
            if not None, is the path to the folder where the .json
            file will be written
        """
        name = 'cmaes_status_g_{}.json'.format(self._g)
        if path:
            name = os.path.join(path, name)
        data = self._prepare_json_data()
        with open(name, 'w') as fp:
            json.dump(data, fp, cls=GeneralizedEncoder)

    def as_dict(self):
        """ Returns a dictionary with the parameters of the
        ``CMAES`` instance """
        params = dict()
        params['mean'] = self.m.copy()
        params['covariance'] = self.C.copy()
        params['step_size'] = self.step_size
        params['random_seed'] = self._random_seed
        params['g'] = self.g
        params['p_sigma'] = self._p_sigma
        params['p_c'] = self._p_c
        params['step_size_0'] = self._step_size_0
        return params

    @staticmethod
    def _read_json_wrap(json_status):
        with open(json_status, 'r') as fp:
            data = json.load(fp)
        for key, value in data['cmaes'].items():
            if key in ['mean', 'covariance', 'p_sigma', 'p_c']:
                data['cmaes'][key] = np.array(value)
        return data

    @classmethod
    def load_status(cls, json_status):
        """ From a CMAES status saved as json, returns a CMAES instance
        initialized with the information contained in ``json_status``"""
        data = cls._read_json_wrap(json_status)
        for key in data:
            for key2, value2 in data[key].items():
                if isinstance(value2, list):
                    data[key][key2] = np.array(value2)
        cmaes_data = {key: value for (key, value) in data['cmaes'].items()
                      if key in cls.cmaes_parameters}
        strategy_params = StrategyParameters(**data['StrategyParameters'])
        termination_criteria = TerminationCriteria(
            **data['TerminationCriteria'])
        cmaes = cls(strategy_params=strategy_params,
                    terminator=termination_criteria,
                    **cmaes_data)
        cmaes._g = data['cmaes']['g']
        cmaes._p_c = data['cmaes']['p_c']
        cmaes._p_sigma = data['cmaes']['p_sigma']
        return cmaes


class GpCMAES(CMAES):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._p_g = np.zeros_like(self.m)

    @property
    def gradients(self):
        return self._gradients.copy()

    def _get_gradients(self):
        mu = self.StrategyParameters.mu
        shape = (mu, self.dimension)
        all_grads = self._fitness_calculator.get_gradients()
        if not all_grads.shape == (self.pop_size, self.dimension):
            raise ValueError('The array shape must be: ({}, {}) '.format(
                self.pop_size, self.dimension))
        # order the gradients according to the fitness
        grads = np.empty(shape)
        fitnesses = self._fitness_calculator.fitnesses
        indices = np.argsort(-np.array(fitnesses))
        for i, ind in enumerate(indices[:mu]):
            grads[i] = all_grads[ind]
        weights = self.StrategyParameters.weights[:mu]
        self._gradients = grads.copy()
        self._f_gradient = (weights[:, np.newaxis]*grads).sum(axis=0)

    @property
    def gradient_coefficient(self):
        """ The parameter controlling the gradient relevance"""
        return self._alpha_gradient

    def set_gradient_coefficient(self, alpha):
        """ Set the coefficient that multiplies the average gradient in the
        update of the mean.

        Parameters
        ----------
        alpha : float
        """
        self._alpha_gradient = alpha
        self._alpha_gradient_0 = alpha

    def _update_gradient_term(self):
        self._get_gradients()
        if hasattr(self, 'c_g'):
            c_g = self.c_g
        else:
            c_g = self.StrategyParameters.c_g
            if c_g is None:
                c_g = 0.1*self._step_size_0
                self.c_g = c_g
        f_gradient = self._f_gradient
        norm = self._expected_norm_standard
        norm_g = np.linalg.norm(f_gradient)
        scaling = math.exp(c_g*(1 - norm_g*self.step_size/norm))
        self._alpha_gradient *= scaling

    def _update_mean(self):
        self._update_gradient_term()
        grad_term = self._alpha_gradient*self._f_gradient
        self._yw = self._yw - grad_term
        self._m = (self._m
                   + self.StrategyParameters.c_m*self.step_size*self._yw)

    def as_dict(self):
        params = super().as_dict()
        params['cmaes_grad'] = {'alpha_gradient': self._alpha_gradient,
                                'alpha_gradient_0': self._alpha_gradient_0}
        return params

    @classmethod
    def load_status(cls, json_status):
        """ From a CMAES status saved as json, returns a CMAES instance
        initialized with the information contained in ``json_status``"""
        cmaes = super().load_status(json_status)
        data = cls._read_json_wrap(json_status)
        cmaes._step_size_0 = data['cmaes']['step_size_0']
        data = data['cmaes']['cmaes_grad']
        cmaes.set_gradient_coefficient(data['alpha_gradient'])
        cmaes._alpha_gradient_0 = data['alpha_gradient_0']
        return cmaes
