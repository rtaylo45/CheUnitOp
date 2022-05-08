import numpy as np
import scipy.linalg
from abc import ABC, abstractmethod
import CheUnitOp.solvers.matrixExponential.factory as matExp


class ODESolverBase(ABC):
    """Something"""

    def __init__(self, **kwargs):
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

    
    def __init__(self, **kwargs):
        super(ODELinearSolverBase, self).__init__(**kwargs)


class ODEExponentialTimeDifferencing(ODELinearSolverBase):
    """Something"""
    
    isExponentialTimeDifferencing = True


    def __init__(self, **kwargs):
        """Something"""
        super(ODEExponentialTimeDifferencing, self).__init__(**kwargs)
        self.matrixExp = scipy.linalg

    
    def solve(self, A, b, dt):
        return self.matrixExp.expm(A * dt) @ b


    def preSolve(self):
        pass


    def postSolve(self):
        pass


def Factory(solverName, **kwargs):
    solverOptions = {
        "scipy": ODEExponentialTimeDifferencing
    }
    return solverOptions[solverName](**kwargs)

