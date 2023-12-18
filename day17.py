from collections import defaultdict
from math import inf
import heapq


def reverse(direction):
    rev = {"N": "S", "S": "N", "E": "W", "W": "E", "X": "X"}
    return rev[direction]


def move(point, direction, bounds):
    if direction == "N" and point[0] != 0:
        return (point[0] - 1, point[1])
    if direction == "S" and point[0] != bounds[0] - 1:
        return (point[0] + 1, point[1])
    if direction == "W" and point[1] != 0:
        return (point[0], point[1] - 1)
    if direction == "E" and point[1] != bounds[1] - 1:
        return (point[0], point[1] + 1)
    return False


def is_valid(directions, voisin):
    if voisin == reverse(directions[-1]):
        return False
    if all([d == voisin for d in directions]):  # Must turn
        return False
    if any([d != directions[-1] for d in directions[-4:]]) and voisin != directions[-1]:
        return False
    return True


def dijkstra(graphe, src, dst, part1=True) -> int:
    bounds = (len(graphe), len(graphe[0]))
    vus = defaultdict(lambda: False)
    sac = []
    heapq.heappush(sac, (0, src, src, "XXXXXXXXXX"))
    while len(sac) > 0:
        distance, sommet, parent, direction = heapq.heappop(
            sac
        )  # on extrait un sommet du sac
        if sommet == dst and (part1 or all([d == direction[-1] for d in direction[-4:]])
        ):
            # vus[sommet, direction] = True
            return distance  # on est arrivé
        if not vus[sommet, direction]:  # si c'est la première fois qu'on le voit
            vus[sommet, direction] = True  # on le marque comme vu
            if part1:
                for voisin in ["N", "S", "E", "W"]:
                    if reverse(direction[-1]) == voisin:  # No reversing
                        pass
                    elif (
                        voisin == direction[-1]
                        and voisin == direction[-2]
                        and voisin == direction[-3]
                    ):  # Straight line
                        pass
                    else:
                        next_sommet = move(sommet, voisin, bounds)
                        if next_sommet:
                            heapq.heappush(
                                sac,
                                (
                                    graphe[next_sommet[0]][next_sommet[1]] + distance,
                                    next_sommet,
                                    sommet,
                                    direction[-2:] + voisin,
                                ),
                            )  # on met ses voisins dans le sac
            else:
                for voisin in ["N", "S", "E", "W"]:
                    if is_valid(direction, voisin):
                        next_sommet = move(sommet, voisin, bounds)
                        if next_sommet:
                            heapq.heappush(
                                sac,
                                (
                                    graphe[next_sommet[0]][next_sommet[1]] + distance,
                                    next_sommet,
                                    sommet,
                                    direction[-9:] + voisin,
                                ),
                            )  # on met ses voisins dans le sac
    return inf  # on n'a pas réussi à atteindre la destination


with open("input/input17.txt", "r") as f:
    city = [[int(x) for x in row] for row in f.read().splitlines()]

distance = dijkstra(city, (0, 0), (len(city) - 1, len(city[0]) - 1))

print("Partie 1:", distance)

distance = dijkstra(city, (0, 0), (len(city) - 1, len(city[0]) - 1), False)

print("Partie 2:", distance)
