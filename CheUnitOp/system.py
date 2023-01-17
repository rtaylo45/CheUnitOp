from collections.abc import Iterable

import numpy as np
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt

from CheUnitOp.species import ComponentSpecies
import CheUnitOp.solvers.base as CheUnitOpSolver

class GenericSystem:
    """
    This object is the driver for the simulation. It holds all components,
    sets up and solves the proble, and handels output.

    Args:
        name:               Name of the system
        volumetricFlowRate: Volumetric flow rate of the system in units of m^3/s
    """
    def __init__(self, name, volumetricFlowRate):
        assert(isinstance(name, str))
        assert(volumetricFlowRate >= 0.0)
        self.name = name
        self.volumetricFlowRate = volumetricFlowRate
        self.globalSpecies = []
        self.components = []
        self.boundaryComponents = []
        self.solver = CheUnitOpSolver.Factory("scipy")
        self.areComponentFinalized = False
        self.areSpeciesFinalized = False
        self.solutionData = None
        self.timeSteps = None

    def addSpecies(self, species):
        """
        Adds a single species or adds a list of species to the model

        Args:
            species: List of species or single species object to add to the model
        """
        assert(not self.areSpeciesFinalized)
        if isinstance(species, Iterable):
            for spec in species:
                self.globalSpecies.append(spec)
        else:
            self.globalSpecies.append(species)

    def addComponents(self, components):
        """
        Adds a single component or list of components

        Args:
            components: List of components or single component to add to the model
        """
        assert(not self.areComponentFinalized)
        if isinstance(components, Iterable):
            for component in components:
                component.setVolumetricFlowRate(self.volumetricFlowRate)
                if component.isBoundaryComponent:
                    self.boundaryComponents.append(component)
                else:
                    self.components.append(component)
        else:
            components.setVolumetricFlowRate(self.volumetricFlowRate)
            if component.isBoundaryComponent:
                self.boundaryComponents.append(component)
            else:
                self.components.append(components)

    def addConnection(self, feedComponent, targetComponent, feedComponentFraction):
        """
        Adds a connection between two components passed as a list or single values.

         ----------------          ------------------
        |                |        |                  |
        | feed component | -----> | target component |
        |                |        |                  |
         ----------------          ------------------

        Args:
            feedComponent:         Component that feeds the inlet component
            inletComponent:        Component that receives the feed
            feedComponentFraction: Fraction of flow from feed component that goes
                                   into the inlet component
        """
        assert(not self.areComponentFinalized)
        # Adds inlet flow for target component
        targetComponent.addFlowComponent(feedComponentFraction, feedComponent, "inlet")
        # Adds the outlet flow for the feed component
        feedComponent.addFlowComponent(feedComponentFraction, targetComponent, "outlet")

    def addBoundaryInletFlow(self, speciesNamesCons, boundaryTank):
        """
        Adds an inlet flow boundary condition to the model. This function must
        be called.

        Args:
            speciesNamesCons: tuple or list of tuples for species inlet boundary
                              conditions. The tuple takes this form:
                              (species Name, species concentrations kg/m^3).
        """
        pass

    def addBoundaryOutletFlow(self):
        """
        Adds an outlet flow boundary condition to the model. It is assumed that
        all species flow out of this tank so no species or concentrations need to
        be passed in.
        """
        pass

    def setSolver(self, solverName):
        """
        Sets the solver for the system

        Args:
            solverName: The solver object name
        """
        self.solver = CheUnitOpSolver.Factory(solverName)

    def solve(self, tEnd, numSteps):
        """
        Solves the system for species masses. Assumes that the start time is 0

        Args:
            tEnd:     End time of the simulation
            numSteps: Number of steps to take
        """
        A = self.__buildTransitionMatrix()
        dt = tEnd/float(numSteps)
        A = A.toarray()
        for step in range(1, numSteps+1):
            b = self.__buildInitialCondition()
            sol = self.solver.solve(A, b, dt)
            self.__unpackSolution(sol)
        # Unpacks the final solution to a dict for easy access
        self.__buildSolutionData()
        self.timeSteps = np.linspace(0, tEnd, numSteps+1)

    def plot(self, componentName = None, speciesName = None):
        """
        Plots the solution
        """
        if (speciesName and not componentName):
            for component in self.components:
                solution = self.getSolution(component.name, speciesName)
                plt.plot(self.timeSteps, solution, label = "Tank A")

            plt.legend()
            plt.grid()
            plt.title(f"{speciesName}")
            plt.xlabel("Time [sec]")
            plt.ylabel("Concentration")
            plt.savefig(f"{self.name}_species_concentrations_in_operations.png")
        
        else:
            print("Something went wrong")
            exit()


    def getSolution(self, componentName = None, speciesName = None):
        """
        Gets the soltuion
        """
        assert(self.solutionData)
        if (componentName and not speciesName):
            return self.solutionData[componentName]
        elif (componentName and speciesName):
            return self.solutionData[componentName][speciesName]
        else:
            return self.soltuionData

    def finalizeComponents(self):
        """
        Finilizes the system components
        """
        for cID, component in enumerate(self.components):
            component._checkInletOutletFlowRates()
            component.ID = cID

        self.areComponentFinalized = True

    def finalizeSpecies(self):
        """
        Finilizes the species in the system
        """
        totalComponents = self.components + self.boundaryComponents
        componentNames = [component.name for component in totalComponents]
        for component in totalComponents:
            for sID, spec in enumerate(self.globalSpecies):
                componentInitialMass = 0.0
                spec.ID = sID
                for initialComponentConcentrationTupe in spec.componentInitialConcentration:
                    componentName = initialComponentConcentrationTupe[0]
                    assert(componentName in componentNames)
                    if componentName == component.name:
                        componentInitialCon = initialComponentConcentrationTupe[1]
                component.addSpecies(ComponentSpecies(spec.name, spec.molarMass,
                component.name, sID, componentInitialCon))

        self.areSpeciesFinalized = True

    def printInfo(self):
        """
        Prints information about the system.
        """
        print("################################################################")
        print("System Information")
        print("Name: " + self.name)
        print("Volumetric flow rate (m^3/s): " + str(self.volumetricFlowRate))
        print("Number of components: " + str(len(self.components)))
        print("Number of speices: " + str(len(self.globalSpecies)))
        print("################################################################")
        for component in self.components:
            component.printInfo()
            print("############################")

    def __buildTransitionMatrix(self):
        """
        Builds the transition matrix (A) for dy / dt = A * y
        """
        DOFs = len(self.globalSpecies) * len(self.components)
        numSpecies = len(self.globalSpecies)
        A = np.zeros((DOFs, DOFs))
        for thisComponent in self.components:
            for thisSpecies in thisComponent.species:
                # gets i matrix diagional coefficient
                i = self.__getAj(thisComponent.ID, thisSpecies.ID, numSpecies)
                # i,i coefficient
                thisCoeff = 0.0
                # source term
                thisSpeciesSource = 0.0

                # Loops over the component connections going into this component
                for otherComponentTuple in thisComponent.inletComponents:
                    otherComponentFlowFraction = otherComponentTuple[0]
                    otherComponent = otherComponentTuple[1]
                    if otherComponent.isBoundaryComponent:
                        thisSpeciesSource += (otherComponent.species[thisSpecies.ID].getCon() *
                        self.volumetricFlowRate * otherComponentFlowFraction)
                    else:
                        transCoeff = (self.volumetricFlowRate * otherComponentFlowFraction
                        / thisComponent.volume)
                        j = self.__getAj(otherComponent.ID, thisSpecies.ID, numSpecies)
                        A[i,j] = transCoeff

                # Loops over the component connections going out this component
                for otherComponentTuple in thisComponent.outletComponents:
                    otherComponentFlowFraction = otherComponentTuple[0]
                    otherComponent = otherComponentTuple[1]
                    thisCoeff -= (self.volumetricFlowRate * otherComponentFlowFraction
                    / thisComponent.volume)
                A[i,i] = thisCoeff
        return csr_matrix(A)

    def __buildInitialCondition(self):
        """
        Builds the initial condition (b) for dy / dt = A * y
        """
        DOFs = len(self.globalSpecies) * len(self.components)
        b = np.zeros((DOFs, 1))
        i = 0
        for thisComponent in self.components:
            for thisSpecies in thisComponent.species:
                b[i] = thisSpecies.getCon()
                i += 1
        return b

    def __unpackSolution(self, sol):
        """
        Unpacks the solution

        Args:
            sol: The solution vector
        """
        i = 0
        for thisComponent in self.components:
            for thisSpecies in thisComponent.species:
                thisSpecies.addCon(float(sol[i]))
                i += 1

    def __buildSolutionData(self):
        """
        Builds the soltuion data dictionary for easy access to solution data
        """
        self.solutionData = {}
        for thisComponent in self.components:
            self.solutionData[thisComponent.name] = {}
            for thisSpecies in thisComponent.species:
                self.solutionData[thisComponent.name][thisSpecies.name] = thisSpecies.concentrations

    def __getAj(self, solutionComponentIndex, speciesIndex, totalSpecies):
        rowsBefore = solutionComponentIndex * totalSpecies
        return rowsBefore + speciesIndex
