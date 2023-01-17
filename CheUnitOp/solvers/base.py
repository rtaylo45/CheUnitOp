import numpy as np
import scipy.linalg
from abc import ABC, abstractmethod


class ODESolverBase(ABC):
    """Something"""

    def __init__(self, *kargs, **kwargs):
        pass

    @abstractmethod
    def solve(self, A, b, dt):
        pass

    @abstractmethod
    def preSolve(self):
        pass

    @abstractmethod
    def postSolve(self):
        pass


class ODELinearSolverBase(ODESolverBase):
    """Something"""

    isLinearSolver = True

    
    def __init__(self, *kargs, **kwargs):
        super(ODELinearSolverBase, self).__init__(*kargs, **kwargs)


class ODEExponentialTimeDifferencingBase(ODELinearSolverBase):
    """Something"""
    
    isExponentialTimeDifferencing = True


    def __init__(self, matrix_type='static', dt_type='static', *kargs, **kwargs):
        """Something"""
        super(ODEExponentialTimeDifferencingBase, self).__init__(*kargs, **kwargs)
        self.matrix_type = matrix_type
        self.dt_type = dt_type

    def solve(self, A, b, dt):
        pass

    def preSolve(self):
        pass

    def postSolve(self):
        pass

