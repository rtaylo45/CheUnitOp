from abc import ABC
from numpy import isclose
from collections.abc import Iterable
from sys import exit

class ComponentBase(ABC):
    """
    Abstract class that all components must inherit from. A componet is a
    unit operation within the system. Inlet and outlet components are list of
    tuples (fraction, component)

    Args:
        name:               Name of the component
        volume:             Volume of the component in m^3
    """

    def __init__(self, name, volume):
        assert(isinstance(name, str))
        assert(volume >= 0.0)
        self.name = name
        self.volume = volume
        self.volumetricFlowRate = 0.0
        self.inletComponents = []
        self.outletComponents = []
        self.species = []
        self.isBoundaryComponent = False
        self.ID = -1

    def addFlowComponent(self, flowFractions, components, direction):
        """
        Adds a single or multiple inlet/outlet components to this component. This
        function should not be used by the user.

        Args:
            flowFractions: Flow fractions associated with the inlet components
            components:    Components that feed this component
            direction:     The direction of flow for this connection.
        """
        if isinstance(flowFractions, Iterable):
            assert(len(flowFractions) == len(components))
            for i in range(len(flowFractions)):
                flowFractionComponentTuple = (flowFractions[i], components[i])
                if direction == 'inlet':
                    self.inletComponents.append(flowFractionComponentTuple)
                elif direction == 'outlet':
                    self.outletComponents.append(flowFractionComponentTuple)
                else:
                    exit("Direction {"+direction+"} is not valid. Either use inlet or outlet")
        else:
            flowFractionComponentTuple = (flowFractions, components)
            if direction == 'inlet':
                self.inletComponents.append(flowFractionComponentTuple)
            elif direction == 'outlet':
                self.outletComponents.append(flowFractionComponentTuple)
            else:
                exit("Direction {"+direction+"} is not valid. Either use inlet or outlet")

    def setVolumetricFlowRate(self, volumetricFlowRate):
        """
        Sets the volumetric flow rate going into or out of the component.

        Args:
            volumetricFlowRate: Volumetric flow rate of the system m^3/s
        """
        assert(volumetricFlowRate >= 0.0)
        self.volumetricFlowRate = volumetricFlowRate

    def printInfo(self):
        """
        Prints information about the component.
        """
        print("Component Name: " + self.name)
        print("Volume (m^3): " + str(self.volume))
        print("Species: ")
        for spec in self.species:
            print("\t " + spec.name + ": Initial Mass: " + str(spec.initialMass))
        print("Inlet Components:")
        for componentTuple in self.inletComponents:
            print("\t Name: " + componentTuple[1].name)
            print("\t Flow fraction: " + str(componentTuple[0]) + "\n")
        print("Outlet Components:")
        for componentTuple in self.outletComponents:
            print("\t Name: " + componentTuple[1].name)
            print("\t Flow fraction: " + str(componentTuple[0]) + "\n")

    def addSpecies(self, species):
        """
        Adds a species to a component. This function should only be used by
        the system object. The user should never use this function.

        Args:
            species: Component species object that gets added.
        """
        self.species.append(species)

    def _checkInletOutletFlowRates(self):
        """
        Checks the inlet and outlet volumetric flow rates to make sure they
        equal one another. This is to make sure that the liquid volume of the
        tank does not change with time, as this is an assumption when solving
        the ODEs.
        """
        inletVolumeFlowRate = 0.0
        for flowComponentTuple in self.inletComponents:
            inletVolumeFlowRate += flowComponentTuple[0] * self.volumetricFlowRate
        outletVolumeFlowRate = 0.0
        for flowComponentTuple in self.outletComponents:
            outletVolumeFlowRate += flowComponentTuple[0] * self.volumetricFlowRate
        assert(isclose(inletVolumeFlowRate, outletVolumeFlowRate))

class InletBoundaryCondition(ComponentBase):
    """
    Adds an inlet boundary condition to the system by adding a fictitous tank
    to the system to allow for species to flow in.

    Args:
        name: Name of the inlet boundary condition
    """
    def __init__(self, name = "Inlet Boundary Condition"):
        super(InletBoundaryCondition, self).__init__(name, 1.0)
        self.isBoundaryComponent = True

    def _checkInletOutletFlowRates(self):
        """
        Over rides the base class check inlet/outlet flow rates because the
        inlet and outlet flow rates will not be equal.
        """
        pass


class OutletBoundaryCondition(ComponentBase):
    """
    TODO: This class might not be necessary

    Adds an outlet boundary condition to the system, allowing species to flow
    out of the system.

    Args:
        name: Name of the outlet boundary condition
    """
    def __init__(self, name = "Outlet Boundary Condition"):
        super(OutletBoundaryCondition, self).__init__(name, 1.0)
        self.isBoundaryComponent = True

    def _checkInletOutletFlowRates(self):
        """
        Over rides the base class check inlet/outlet flow rates because the
        inlet and outlet flow rates will not be equal.
        """
        pass

class GenericTank(ComponentBase):
    """
    A generic tank that hold fluid and allows for species to flow into, mix and
    flow out.
    """
    pass
