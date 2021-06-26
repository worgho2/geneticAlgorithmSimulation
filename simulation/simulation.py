from random import random, randint
from time import sleep
from place import Place, print_places
import genetic_algorithm as GA
import fuzzy as FUZZY
import matplotlib.pyplot as plt

# GENETIC ALGORITHM PARAMETERS
population_size = 100
number_of_parents = 10
probability_of_mutation = 0.05
number_of_rouds = 100

fuel_level = randint(50, 100)

verbose = True

origin, places = Place.from_file("places.txt")
print('\nORIGIN:')
print(origin)
print('\nHEALTH UNITS:')
print_places(places)

print(
    '\nPARAMETERS:',
    '\npopulation_size:', population_size,
    '\nnumber_of_parents:', number_of_parents,
    '\nprobability_of_mutation:', probability_of_mutation,
    '\nnumber_of_rounds:', number_of_rouds,
    '\nverbose:', verbose
)

input('\n----- press ENTER to start ----- ')


population = GA.population(places, population_size, verbose)

for i in range(number_of_rouds):
    population = GA.selection_and_crossover(
        population,
        number_of_parents,
        lambda x: GA.hs_fitness(x, origin),
        verbose
    )
    population = GA.mutation(
        population,
        number_of_parents,
        probability_of_mutation,
        verbose
    )

route = GA.best_chromossome(
    population,
    lambda x: GA.hs_fitness(x, origin),
    verbose
)
GA.print_route(route, origin)

while len(route) > 1:
    total_remaining_distance = GA.hs_fitness(route, origin)
    recommendation = FUZZY.simulate(fuel_level, total_remaining_distance)
    fuel_level -= 10
    print('\nROUTE CALCULATED RISK:', recommendation)

    print(
        '\nSELECT ONE ACTION:',
        '\n(1) PROCEED',
        '\n(2) GIVE UP A PLACE AND RECALCULATE ROUTE'
        '\n(3) GIVE UP TWO PLACES AND RECALCULATE ROUTE',
        '\n(4) ABORT'
    )

    action_input = input('-> ')

    plt.close("all")

    if action_input == '2':
        if len(route) < 3:
            print('\nOPERATION DENIED')
            sleep(2)
            continue
        removed = randint(0, len(route)-1)
        route.pop(removed)
        population = GA.population(route, population_size, verbose)
        for i in range(number_of_rouds):
            population = GA.selection_and_crossover(
                population,
                number_of_parents,
                lambda x: GA.hs_fitness(x, origin),
                verbose
            )
            population = GA.mutation(
                population,
                number_of_parents,
                probability_of_mutation,
                verbose
            )
        route = GA.best_chromossome(
            population,
            lambda x: GA.hs_fitness(x, origin),
            verbose
        )

    elif action_input == '3':
        if len(route) < 4:
            print('\nOPERATION DENIED')
            sleep(2)
            continue
        for i in range(2):
            removed = randint(0, len(route)-1)
            route.pop(removed)
        population = GA.population(route, population_size, verbose)
        for i in range(number_of_rouds):
            population = GA.selection_and_crossover(
                population,
                number_of_parents,
                lambda x: GA.hs_fitness(x, origin),
                verbose
            )
            population = GA.mutation(
                population,
                number_of_parents,
                probability_of_mutation,
                verbose
            )
        route = GA.best_chromossome(
            population,
            lambda x: GA.hs_fitness(x, origin),
            verbose
        )
    elif action_input == '4':
        print('\nOPERAÇÃO ABORTADA')
        exit(0)
    else:
        origin = route.pop(0)

    GA.print_route(route, origin)
