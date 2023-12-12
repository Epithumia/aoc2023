from functools import cache
from itertools import combinations


@cache
def is_empty_col(col):
    if any([row[col] == "#" for row in universe]):
        return False
    return True


@cache
def is_empty_row(row):
    if any([c == "#" for c in universe[row]]):
        return False
    return True


def distance(g1, g2, factor):
    return sum(
        [
            factor if is_empty_row(i) else 1
            for i in range(min(g1[0], g2[0]), max(g1[0], g2[0]))
        ]
    ) + sum(
        [
            factor if is_empty_col(i) else 1
            for i in range(min(g1[1], g2[1]), max(g1[1], g2[1]))
        ]
    )


with open("input/input11.txt", "r") as f:
    universe = f.read().splitlines()

galaxies = []

for i in range(len(universe)):
    for j in range(len(universe[i])):
        if universe[i][j] == "#":
            galaxies.append((i, j))

sum_distance = expanded_sum_distance = 0

for g1, g2 in combinations(galaxies, 2):
    sum_distance += distance(g1, g2, 2)
    expanded_sum_distance += distance(g1, g2, 1000000)

print("Partie 1 :", sum_distance)
print("Partie 2 :", expanded_sum_distance)
