# -*- coding: utf-8 -*-
""" Uniformly distributed arm in [0, 1], or [lower, lower + amplitude]."""

__author__ = "Lilian Besson"
__version__ = "0.6"

from random import random
from numpy.random import random as nprandom

from .Arm import Arm
from .kullback import klBern


class Uniform(Arm):
    """ Uniformly distributed arm, default in [0, 1],

    - default to (mini, maxi),
    - or [lower, lower + amplitude], if (lower=lower, amplitude=amplitude) is given.

    >>> arm_0_1 = Uniform()
    >>> arm_0_10 = Uniform(0, 10)  # maxi = 10
    >>> arm_2_4 = Uniform(2, 4)
    >>> arm_m10_10 = Uniform(-10, 10)  # also Uniform(lower=-10, amplitude=20)
    """

    def __init__(self, mini=0., maxi=1., lower=0., amplitude=1.):
        """New arm."""
        self.min = min(mini, lower)  #: Lower value of rewards
        self.lower = mini  #: Lower value of rewards
        self.max = max(maxi, amplitude - lower)  #: Higher value of rewards
        self.amplitude = maxi - mini  #: Amplitude of rewards
        # self.mean = self.min + (self.max - self.min) / 2.0  # Other formula
        self.mean = self.lower + (self.amplitude / 2.0)  #: Mean for this Uniform arm

    # --- Random samples

    def draw(self, t=None):
        """ Draw one random sample. The parameter t is ignored in this Arm."""
        return self.lower + (random() * self.amplitude)

    def draw_nparray(self, shape=(1,)):
        """ Draw a numpy array of random samples, of a certain shape."""
        return self.lower + (nprandom(shape) * self.amplitude)

    # --- Printing

    def __str__(self):
        return "Uniform"

    def __repr__(self):
        return "U({:.3g}, {:.3g})".format(self.lower, self.amplitude)

    # --- Lower bound

    @staticmethod
    def kl(x, y):
        """ The kl(x, y) to use for this arm."""
        return klBern(x, y)

    @staticmethod
    def oneLR(mumax, mu):
        """ One term of the Lai & Robbins lower bound for Bernoulli arms: (mumax - mu) / KL(mu, mumax). """
        return (mumax - mu) / klBern(mu, mumax)


__all__ = ["Uniform"]
