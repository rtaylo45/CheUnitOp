import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import sys

from CheUnitOp.system import GenericSystem
from CheUnitOp.component import GenericTank, InletBoundaryCondition, OutletBoundaryCondition
from CheUnitOp.species import Species

def ODE_solve(t_end, steps):
    v_dot = 10
    tank_1_volume = 20
    tank_2_volume = 40
    tank_3_volume = 60
    C0 = [1000, 0, 0]
    def model(C, t):
        c1, c2, c3 = C[0], C[1], C[2]
        dc1dt = -c1*v_dot/tank_1_volume
        dc2dt = c1*v_dot/tank_2_volume - c2*v_dot/tank_2_volume
        dc3dt = c2*v_dot/tank_3_volume - c3*v_dot/tank_3_volume
        return [dc1dt, dc2dt, dc3dt]
    t = np.linspace(0, t_end, steps)
    C = odeint(model, C0, t)
    return C[:,0], C[:,1], C[:,2]

testSystem = GenericSystem("Test", 10)

tankA = GenericTank("Tank A", 20)
tankB = GenericTank("Tank B", 40)
tankC = GenericTank("Tank C", 60)
inlet = InletBoundaryCondition("Inlet")
outlet = OutletBoundaryCondition("Outlet")

testSystem.addComponents([tankA, tankB, tankC, inlet, outlet])

testSystem.addConnection(inlet, tankA, 1.0)
testSystem.addConnection(tankA, tankB, 1.0)
testSystem.addConnection(tankB, tankC, 1.0)
testSystem.addConnection(tankC, outlet, 1.0)

testSystem.finalizeComponents()

salt = Species("Salt", componentInitialConcentration = [('Tank A', 1000),
                                                        ('Tank B', 0.0),
                                                        ('Tank C', 0.0)])

salt.addInitialConcentrations(("Inlet", 0.0))

testSystem.addSpecies(salt)

testSystem.finalizeSpecies()

testSystem.solve(20, 100)

solTank1 = testSystem.getSolution("Tank A", "Salt")
solTank2 = testSystem.getSolution("Tank B", "Salt")
solTank3 = testSystem.getSolution("Tank C", "Salt")

tank1, tank2, tank3 = ODE_solve(20, 101)

#t = np.linspace(0, 20, 101)
#plt.plot(t, tank1, label = "Tank A")
#plt.plot(t, tank2, label = "Tank B")
#plt.plot(t, tank3, label = "Tank C")
#plt.plot(t, solTank1, label = "Tank A LIO")
#plt.plot(t, solTank2, label = "Tank B LIO")
#plt.plot(t, solTank3, label = "Tank C LIO")
#plt.legend()
#plt.grid()
#plt.xlabel("Time [sec]")
#plt.ylabel("Concentration")
#plt.show()

testSystem.plot(speciesName='Salt')
