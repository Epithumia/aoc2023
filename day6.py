from functools import reduce
from math import sqrt, floor, ceil

with open("input/input6.txt", "r") as f:
    data = f.read().splitlines()

temps = [int(x) for x in ",".join(data[0].split()).split(",")[1:]]
distances = [int(x) for x in ",".join(data[1].split()).split(",")[1:]]


def calculate(race, distance):
    b1 = max(0, 0.5 * (race - sqrt(race**2 - 4 * distance)))
    b2 = min(race, 0.5 * (sqrt(race**2 - 4 * distance) + race))
    choices = floor(b2) - ceil(b1) + 1
    if floor(b1) == ceil(b1):
        choices -= 1
    if floor(b2) == ceil(b2):
        choices -= 1
    choices = max(choices, 0)
    return choices


print(
    "Partie 1:",
    reduce(
        lambda x, y: x * y,
        [calculate(temps[i], distances[i]) for i in range(len(temps))],
    )
)

temps = int("".join([str(x) for x in temps]))
distance = int("".join([str(x) for x in distances]))

print("Partie 2:", calculate(temps, distance))
