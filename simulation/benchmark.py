import genetic_algorithm as GA
from place import Place

import numpy as np
import matplotlib.pyplot as plt

x = []
y = []

population_size = 200
number_of_parents = 10
probability_of_mutation = 0.1
verbose = False

origin, places = Place.from_file("places.txt")

for number_of_rounds in range(1, 100, 5):
    population = GA.population(places, population_size, verbose)

    for i in range(number_of_rounds):
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

    x.append(number_of_rounds)
    y.append(GA.hs_fitness(route, None))


fig, ax = plt.subplots()
ax.plot(x, y)

ax.set(xlabel='number of rounds', ylabel='distance')
ax.grid()

# fig.savefig("test.png")
plt.show()


# plt.scatter(x, y)
# plt.show()
