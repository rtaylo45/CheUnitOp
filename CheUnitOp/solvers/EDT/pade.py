import scipy
import numpy

from CheUnitOp.solvers.base import ODEExponentialTimeDifferencingBase


class Pade(ODEExponentialTimeDifferencingBase):

    def __init__(self, *kargs, **kwargs):
        super(Pade, self).__init(*kargs, **kwargs)

    def pade3(self, A, A2):
        pass

    def pade5(self, A, A2, A4):
        pass

    def pade7(selfA, A2, A4, A6):
        pass

    def pade9(self, A, A2, A4, A6, A8):
        pass

    def pad13(self, A, A2, A4, A6):
        pass

    