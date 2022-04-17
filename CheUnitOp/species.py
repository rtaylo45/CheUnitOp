from abc import ABC
from collections.abc import Iterable

class SpeciesBase(ABC):

    def __init__(self, name, molarMass = 0.0):
        assert(isinstance(name, str))
        assert(molarMass >= 0.0)
        self.name = name
        self.molarMass = molarMass
        self.ID = -1

    def printInfo(self):
        """
        Prints information about the species
        """
        print("Species name: " + self.name)
        print("Species molar mass: " + str(self.molarMass))

class Species(SpeciesBase):

    def __init__(self, name, molarMass = 0.0, componentInitialConcentration = []):
        super(Species, self).__init__(name, molarMass)
        for tuple in componentInitialConcentration:
            self.__checkComponentConcentrationTuple(tuple)
        self.componentInitialConcentration = componentInitialConcentration

    def addInitialConcentrations(self, componentConcentrationTuples):
        """
        Adds an initial concentration to a species in a component

        Args:
            componentConcentrationTuple: a tuple of component name and species
                                         concentration.
        """
        if len(componentConcentrationTuples) > 2:
            for tuple in componentConcentrationTuples:
                self.__checkComponentConcentrationTuple(tuple)
                self.componentInitialConcentration.append(tuple)
        else:
            self.__checkComponentConcentrationTuple(componentConcentrationTuples)
            self.componentInitialConcentration.append(componentConcentrationTuples)

    def __checkComponentConcentrationTuple(self, tuple):
        """
        Checks to make sure the passed in tuple is valid. It should have two
        values. The first value should be a string, the second should be a real
        value greater than or equal to 0.0.

        Args:
            tuple: Tuple with the component name as the first value and the
                   concentration as the second value.
        """
        assert(len(tuple) == 2)
        assert(isinstance(tuple[0], str))
        assert(tuple[1] >= 0.0)

class ComponentSpecies(SpeciesBase):

    def __init__(self, name, molarMass, componentName, speciesID, initialCon = 0.0):
        super(ComponentSpecies, self).__init__(name, molarMass)
        assert(initialCon >= 0.0)
        self.componentName = componentName
        self.concentrations = [initialCon]
        self.ID = speciesID

    def addCon(self, value):
        """
        Adds a solution to the concentration history

        Args:
            value: The concentration in kg/m^3
        """
        assert(value >= 0.0)
        self.concentrations.append(value)

    def getCon(self):
        """
        Gets the most recent soltuion
        """
        return self.concentrations[-1]
