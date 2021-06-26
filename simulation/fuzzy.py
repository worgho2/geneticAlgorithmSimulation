import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def simulate(fuel_level, total_remaining_distance):

    # Creating variables
    remainingFuel = ctrl.Antecedent(np.arange(0, 101, 1), 'remainingFuel')
    remainingDistance = ctrl.Antecedent(
        np.arange(0, 101, 1), 'remainingDistance')
    routeRisk = ctrl.Consequent(np.arange(0, 101, 1), 'routeRisk')

    # Mapping crisp values to fuzzy values
    # trimf(remainingFuel.universe, [0, 0, 100])
    remainingFuel['almostEmpty'] = fuzz.trapmf(
        remainingFuel.universe,
        [0, 0, 20, 50]
    )
    remainingFuel['hasFuel'] = fuzz.trimf(remainingFuel.universe, [0, 50, 100])
    remainingFuel['full'] = fuzz.trimf(remainingFuel.universe, [50, 100, 100])

    # remainingFuel.view()

    remainingDistance['almostThere'] = fuzz.gaussmf(
        remainingFuel.universe, 0, 15)
    remainingDistance['medium'] = fuzz.gaussmf(remainingFuel.universe, 50, 15)
    remainingDistance['far'] = fuzz.gaussmf(remainingFuel.universe, 100, 20)

    # remainingDistance.view()

    routeRisk['low'] = fuzz.trapmf(routeRisk.universe, [0, 0, 40, 65])
    routeRisk['medium'] = fuzz.trimf(routeRisk.universe, [35, 65, 100])
    routeRisk['high'] = fuzz.trapmf(routeRisk.universe, [65, 80, 100, 100])

    # routeRisk.view()

    # Creating Rules
    rule1 = ctrl.Rule(remainingFuel['almostEmpty'] &
                      remainingDistance['almostThere'], routeRisk['low'])
    rule2 = ctrl.Rule(remainingFuel['almostEmpty'] &
                      remainingDistance['medium'], routeRisk['medium'])
    rule3 = ctrl.Rule(remainingFuel['almostEmpty']
                      & remainingDistance['far'], routeRisk['high'])
    rule4 = ctrl.Rule(remainingFuel['hasFuel'] &
                      remainingDistance['almostThere'], routeRisk['low'])
    rule5 = ctrl.Rule(remainingFuel['hasFuel'] &
                      remainingDistance['medium'], routeRisk['medium'])
    rule6 = ctrl.Rule(remainingFuel['hasFuel'] &
                      remainingDistance['far'], routeRisk['medium'])
    rule7 = ctrl.Rule(
        remainingFuel['full'] & remainingDistance['almostThere'], routeRisk['low'])
    rule8 = ctrl.Rule(remainingFuel['full'] &
                      remainingDistance['medium'], routeRisk['low'])
    rule9 = ctrl.Rule(remainingFuel['full'] &
                      remainingDistance['far'], routeRisk['low'])

    route_ctrl = ctrl.ControlSystem([
        rule1,
        rule2,
        rule3,
        rule4,
        rule5,
        rule6,
        rule7,
        rule8,
        rule9
    ])

    route_simulation = ctrl.ControlSystemSimulation(route_ctrl)

    # Inputs
    route_simulation.input['remainingFuel'] = fuel_level
    route_simulation.input['remainingDistance'] = total_remaining_distance

    route_simulation.compute()

    remainingFuel.view(sim=route_simulation)
    remainingDistance.view(sim=route_simulation)
    routeRisk.view(sim=route_simulation)

    return route_simulation.output['routeRisk']
