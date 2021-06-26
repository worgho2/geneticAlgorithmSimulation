from random import shuffle, randint, random

from coordinate import haversine
from google_maps import Google_maps
from place import print_places


def print_population(population):
    for i in range(len(population)):
        print(list(map(lambda x: x.id, population[i])))


def print_chromosome(chromosome):
    print(list(map(lambda x: x.id, chromosome)))


def print_route(route, origin=None):
    print('\nORIGIN:')
    print(origin)
    print('\nROUTE:')
    print_places(route)
    print('\nGOOGLE MAPS REPRESENTATION:')
    print_route_url(route, origin)


# print google maps route
def print_route_url(chromosome, origin):
    if origin is not None:
        Google_maps.addWaipoint(
            origin.coordinate.latitude,
            origin.coordinate.longitude
        )

    for i in range(len(chromosome)):
        Google_maps.addWaipoint(
            chromosome[i].coordinate.latitude,
            chromosome[i].coordinate.longitude
        )

    print(Google_maps.buildUrl())


# p - population
def best_chromossome(population, fn_fitness, verbose=False):
    p = [(fn_fitness(i), i) for i in population]
    p = [i[1] for i in sorted(p)]

    if verbose:
        print_chromosome(p[0])

    return p[0]


# bp - best population
# br - best route
def print_result(population, fn_fitness):
    print('\nBEST ROUTE:')

    bp = [(fn_fitness(i), i) for i in population]
    bp = [i[1] for i in sorted(bp)]
    br = bp[0]

    print(
        'c:',
        list(map(lambda x: x.id, br)),
        'fitness:',
        fn_fitness(br),
        '\n'
    )
    print_chromosome(br)

    for i in range(len(br)):
        Google_maps.addWaipoint(
            br[i].coordinate.latitude, br[i].coordinate.longitude
        )
    print(Google_maps.buildUrl())


def population(places, size, verbose=False):
    population = [list(places) for i in range(size)]

    for i in population:
        shuffle(i)

    if verbose:
        print_population(population)

    return population


# based on haversine distance between places
def hs_fitness(places, origin):
    fitness = 0

    if origin is not None:
        fitness = haversine(
            origin.coordinate,
            places[0].coordinate
        )

    for i in range(len(places)):
        if i == len(places)-1:
            break
        fitness += haversine(
            places[i].coordinate,
            places[i+1].coordinate
        )
    return fitness


# based on Google Maps route information
# - TODO
def gm_fitness(places, origin):
    return 0


# sp - scored population
# sc - selected chromosome
# nc - new componenets
def selection_and_crossover(population, parents, fn_fitness, verbose=False):
    sp = [(fn_fitness(i), i) for i in population]
    sp = [i[1] for i in sorted(sp, reverse=True)]
    sc = sp[(len(sp) - parents):]

    if verbose:
        print('\nSELECTED CHROMOSOMES:')
        print_population(sc)
        print('\nCROSSOVER:')

    for i in range(len(sp) - parents):
        point = randint(1, len(sp[i]) - 1)
        shuffle(sc)
        nc = list(sc[0])

        rand = randint(0, 1)

        if rand == 0:
            if verbose:
                print('c:')
                print_chromosome(sp[i])

            for j in range(len(nc[:point])):
                sp[i].remove(nc[:point][j])

            if verbose:
                print(
                    'sc:',
                    list(map(lambda x: x.id, sc[0])),
                    'at:',
                    point,
                    '->',
                    list(map(lambda x: x.id, nc[:point])),
                    ' + ',
                    list(map(lambda x: x.id, sp[i]))
                )

            sp[i] = nc[:point] + sp[i]

        else:

            if verbose:
                print('c:')
                print_chromosome(sp[i])

            for j in range(len(nc[point:])):
                sp[i].remove(nc[point:][j])

            if verbose:
                print(
                    'sc:',
                    list(map(lambda x: x.id, sc[0])),
                    'at:',
                    point,
                    '->',
                    list(map(lambda x: x.id, sp[i])),
                    ' + ',
                    list(map(lambda x: x.id, nc[point:]))
                )

            sp[i] = sp[i] + nc[point:]

    return sp


# mp - mutated population
def mutation(population, parents, probability, verbose=False):
    mp = list(population)

    if verbose:
        print('\nMUTATION:')

    for i in range(len(mp) - parents):
        if (random() <= probability):
            j = randint(0, len(mp[i]) - 2)

            if verbose:
                print(
                    'c:',
                    list(map(lambda x: x.id, mp[i])),
                    'c[' + str(j) + ']=' + str(mp[i][j].id),
                    '<-> c[' + str(j+1) + ']=' + str(mp[i][j+1].id),
                    end=' '
                )

            mp[i][j], mp[i][j+1] = mp[i][j+1], mp[i][j]

            if verbose:
                print(
                    '->',
                    list(map(lambda x: x.id, mp[i])),
                )
    return mp
