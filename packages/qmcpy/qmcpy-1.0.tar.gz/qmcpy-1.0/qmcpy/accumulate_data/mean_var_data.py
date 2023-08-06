from ._accumulate_data import AccumulateData
from ..integrand._integrand import Integrand
from time import time
from numpy import *


class MeanVarData(AccumulateData):
    """ Update and store mean and variance estimates. """

    parameters = ['levels','solution','n','n_total','error_bound','confid_int']
    EPS = finfo(float32).eps

    def __init__(self, stopping_crit, integrand, true_measure, discrete_distrib, n_init):
        """
        Args:
            stopping_crit (StoppingCriterion): a StoppingCriterion instance
            integrand (Integrand): an Integrand instance
            true_measure (TrueMeasure): A TrueMeasure instance
            discrete_distrib (DiscreteDistribution): a DiscreteDistribution instance  
            n_init (int): initial number of samples
        """
        self.stopping_crit = stopping_crit
        self.integrand = integrand
        self.true_measure = true_measure
        self.discrete_distrib = discrete_distrib
        # Set Attributes
        if self.integrand.leveltype=='fixed-multi':
            self.levels = len(self.integrand.dimensions)
        else:
            self.levels = 1
        self.solution = nan
        self.muhat = full(self.levels, inf)  # sample mean
        self.sighat = full(self.levels, inf)  # sample standard deviation
        self.t_eval = zeros(self.levels)  # processing time for each integrand
        self.n = tile(n_init, self.levels) # currnet number of samples
        self.n_total = 0  # total number of samples
        self.confid_int = array([-inf, inf])  # confidence interval for solution
        super(MeanVarData,self).__init__()

    def update_data(self):
        """ See abstract method. """
        for l in range(self.levels):
            t_start = time() # time the integrand values
            if self.integrand.leveltype=='fixed-multi':
                # reset dimension
                new_dim = self.integrand._dim_at_level(l)
                self.true_measure._set_dimension_r(new_dim)
                samples = self.discrete_distrib.gen_samples(n=self.n[l])
                y = self.integrand.f(samples,l=l).squeeze()
            else:
                samples = self.discrete_distrib.gen_samples(n=self.n[l])
                y = self.integrand.f(samples).squeeze()
            self.t_eval[l] = max( (time()-t_start)/self.n[l], self.EPS) 
            self.sighat[l] = y.std() # compute the sample standard deviation
            self.muhat[l] = y.mean() # compute the sample mean
            self.n_total += self.n[l] # add to total samples
        self.solution = self.muhat.sum() # tentative solution
