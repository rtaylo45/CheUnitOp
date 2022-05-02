import numpy as np
import scipy.linalg
from abc import ABC, abstractmethod


class ODESolverBase(ABC):
    """Something"""

    def __init__(self):
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

    
    def __init__(self):
        super(LinearSolverBase, self).__init__()


class ODEExponentialTimeDifferencing(ODELinearSolverBase):
    """Something"""
    
    isExponentialTimeDifferencing = True


    def __init__(self):
        """Something"""
        self.matrixExp = scipy.linalg

    
    def solve(self, A, b, dt):
        return self.matrixExp.expm(A * dt) @ b


    def preSolve(self):
        pass


    def postSolve(self):
        pass


def Factory(solverName):
    solverOptions = {
        "scipy": ODEExponentialTimeDifferencing
    }
    return solverOptions[solverName]()

