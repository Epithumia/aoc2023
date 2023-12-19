from collections import defaultdict

with open("input/input18.txt", "r") as f:
    data = f.read().splitlines()


class Brick:
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j


def dig(pool):
    queue = [(1, 1)]
    while len(queue) > 0:
        next_hole = queue.pop()
        if not pool[next_hole]:
            pool[next_hole] = True
            queue.append((next_hole[0] + 1, next_hole[1]))
            queue.append((next_hole[0] - 1, next_hole[1]))
            queue.append((next_hole[0], next_hole[1] + 1))
            queue.append((next_hole[0], next_hole[1] - 1))


pool = defaultdict(lambda: False)
i = j = 0
for row in data:
    r = row.split()
    direction = r[0]
    length = int(r[1])

    for _ in range(length):
        if direction == "U":
            i -= 1
        elif direction == "D":
            i += 1
        elif direction == "L":
            j -= 1
        else:
            j += 1
        pool[i, j] = Brick(i, j)

dig(pool)

print("Partie 1:", len(pool))
