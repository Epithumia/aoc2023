from collections import deque, defaultdict
from functools import lru_cache
from math import inf
import heapq
import tqdm

with open("input/input21.txt", "r") as f:
    garden_map = [[c for c in row] for row in f.read().splitlines()]


H = len(garden_map)
W = len(garden_map[0])


queue = deque()

for i in range(H):
    for j in range(W):
        if garden_map[i][j] == "S":
            start = (i, j)

queue.append((0, start[0], start[1]))

destinations = []

goal = 64
while len(queue) > 0:
    step, i, j = queue.popleft()
    if step == goal and (i, j) not in destinations:
        destinations.append((i, j))
        continue
    if i > 0 and garden_map[i - 1][j] != "#" and (step + 1, i - 1, j) not in queue:
        queue.append((step + 1, i - 1, j))
    if j > 0 and garden_map[i][j - 1] != "#" and (step + 1, i, j - 1) not in queue:
        queue.append((step + 1, i, j - 1))
    if i < H - 1 and garden_map[i + 1][j] != "#" and (step + 1, i + 1, j) not in queue:
        queue.append((step + 1, i + 1, j))
    if j < W - 1 and garden_map[i][j + 1] != "#" and (step + 1, i, j + 1) not in queue:
        queue.append((step + 1, i, j + 1))

print("Partie 1:", len(destinations))

distances = {}
parites = {}


H = len(garden_map)
W = len(garden_map[0])
queue.append((0, start[0], start[1]))
while len(queue) > 0:
    step, i, j = queue.popleft()
    if (i, j) not in distances:
        distances[(i, j)] = step
        parites[i, j] = step % 2
        if i > 0 and garden_map[i - 1][j] != "#" and (step + 1, i - 1, j) not in queue:
            queue.append((step + 1, i - 1, j))
        if j > 0 and garden_map[i][j - 1] != "#" and (step + 1, i, j - 1) not in queue:
            queue.append((step + 1, i, j - 1))
        if (
            i < H - 1
            and garden_map[i + 1][j] != "#"
            and (step + 1, i + 1, j) not in queue
        ):
            queue.append((step + 1, i + 1, j))
        if (
            j < W - 1
            and garden_map[i][j + 1] != "#"
            and (step + 1, i, j + 1) not in queue
        ):
            queue.append((step + 1, i, j + 1))

sub = {
    "A": sum([i for i in parites.values()]),
    "B": sum([1 - i for i in parites.values()]),
}

seuil = 64

sub["ANE"] = 0
sub["BNE"] = 0
sub["ASE"] = 0
sub["BSE"] = 0
sub["ANW"] = 0
sub["BNW"] = 0
sub["ASW"] = 0
sub["BSW"] = 0
for i in range(H):
    for j in range(W):
        if i + j < 65 and (i, j) in parites:
            sub["ANE"] += parites[i, j]
            sub["BNE"] += 1 - parites[i, j]
        if i > 65 and j < i - 65 and (i, j) in parites:
            sub["ASE"] += parites[i, j]
            sub["BSE"] += 1 - parites[i, j]
        if i > 65 and j > 65 and i + j > 131 + 64 and (i, j) in parites:
            sub["ASW"] += parites[i, j]
            sub["BSW"] += 1 - parites[i, j]
        if j > 65 and i < j - 65 and (i, j) in parites:
            sub["ANW"] += parites[i, j]
            sub["BNW"] += 1 - parites[i, j]

# print(
#     "0".rjust(5),
#     str(sub["BSW"]).rjust(5),
#     str(sub["A"] - sub["ANE"] - sub["ANW"]).rjust(5),
#     str(sub["BSE"]).rjust(5),
#     "0".rjust(5),
# )
# print(
#     str(sub["BSW"]).rjust(5),
#     str(sub["A"] - sub["ANE"]).rjust(5),
#     str(sub["B"]).rjust(5),
#     str(sub["A"] - sub["ANW"]).rjust(5),
#     str(sub["BSE"]).rjust(5),
# )
# print(
#     str(sub["A"] - sub["ASE"] - sub["ANE"]).rjust(5),
#     str(sub["B"]).rjust(5),
#     str(sub["A"]).rjust(5),
#     str(sub["B"]).rjust(5),
#     str(sub["A"] - sub["ASW"] - sub["ANW"]).rjust(5),
# )
# print(
#     str(sub["BNW"]).rjust(5),
#     str(sub["A"] - sub["ASE"]).rjust(5),
#     str(sub["B"]).rjust(5),
#     str(sub["A"] - sub["ASW"]).rjust(5),
#     str(sub["BNE"]).rjust(5),
# )
# print(
#     "0".rjust(5),
#     str(sub["BNW"]).rjust(5),
#     str(sub["A"] - sub["ASE"] - sub["ASW"]).rjust(5),
#     str(sub["BNE"]).rjust(5),
#     "0".rjust(5),
# )


goal = 26501365
# goal = 131*2+65

pu = goal // 131

partial_total = ((pu - 1) ** 2) * sub["A"] + (pu**2) * sub["B"]

edge_total = 0
# Four corners
edge_total += sub["A"] - sub["ANE"] - sub["ANW"]
edge_total += sub["A"] - sub["ASE"] - sub["ANE"]
edge_total += sub["A"] - sub["ASW"] - sub["ANW"]
edge_total += sub["A"] - sub["ASE"] - sub["ASW"]

# Type A: pu-1 per edge
edge_total += (pu - 1) * (sub["A"] - sub["ANE"])
edge_total += (pu - 1) * (sub["A"] - sub["ANW"])
edge_total += (pu - 1) * (sub["A"] - sub["ASE"])
edge_total += (pu - 1) * (sub["A"] - sub["ASW"])

# Type B: pu per edge
edge_total += (pu) * (sub["BNE"])
edge_total += (pu) * (sub["BNW"])
edge_total += (pu) * (sub["BSE"])
edge_total += (pu) * (sub["BSW"])


print("Partie 2:", partial_total + edge_total)
