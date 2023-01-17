import scipy
import numpy

from CheUnitOp.solvers.base import ODEExponentialTimeDifferencingBase


class Taylor(ODEExponentialTimeDifferencingBase):

    def __init__(self, m_max=55, p_max=8, *kargs, **kwargs):
        super(Taylor, self).__init__(*kargs, **kwargs)
        self.m_max = m_max
        self.p_max = p_max
        self.theta = self._read_theta()

    def _read_theta(self):
        pass

    def solve(self, A, b, dt):
        pass