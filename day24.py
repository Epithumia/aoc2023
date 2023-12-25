import sympy
from itertools import combinations


class Stone:
    def __init__(self, data) -> None:
        coords = data.split("@")[0].split(",")
        velocity = data.split("@")[1].split(",")
        self.x = int(coords[0])
        self.y = int(coords[1])
        self.z = int(coords[2])
        self.vx = int(velocity[0])
        self.vy = int(velocity[1])
        self.vz = int(velocity[2])

    def __repr__(self) -> str:
        return (
            f"Pos: {self.x},{self.y},{self.z}, velocity: {self.vx},{self.vy},{self.vz}"
        )

    def xy_intercept(self, other: "Stone") -> bool:
        if self.vx * other.vy == self.vy * other.vx:
            return -1, -1, -1, -1
        x = (
            -self.vy * other.vx * self.x
            + self.vx * other.vy * other.x
            + self.vx * other.vx * (self.y - other.y)
        ) / (-self.vy * other.vx + self.vx * other.vy)
        y = (
            self.vy * other.vy * self.x
            - self.vy * other.vy * other.x
            - self.vx * other.vy * self.y
            + self.vy * other.vx * other.y
        ) / (self.vy * other.vx - self.vx * other.vy)
        return (x, y, (x - self.x) / self.vx, (x - other.x) / other.vx)


with open("input/input24.txt", "r") as f:
    data = f.read().splitlines()

stones = [Stone(row) for row in data]

boundaries = [200000000000000, 400000000000000]

nb_xy_collisions = 0
for pair in combinations(stones, 2):
    x, y, tx, ty = pair[0].xy_intercept(pair[1])
    if (
        boundaries[0] <= x <= boundaries[1]
        and boundaries[0] <= y <= boundaries[1]
        and tx >= 0
        and ty >= 0
    ):
        nb_xy_collisions += 1

print(nb_xy_collisions)

x = sympy.symbols("x")
y = sympy.symbols("y")
z = sympy.symbols("z")
vx = sympy.symbols("vx")
vy = sympy.symbols("vy")
vz = sympy.symbols("vz")
t1 = sympy.symbols("t1", integer=True)
t2 = sympy.symbols("t2", integer=True)
t3 = sympy.symbols("t3", integer=True)

# First stone
eq1a = sympy.Eq(24 + 5 * vx, stones[0].x + 5 * stones[0].vx)
eq2a = sympy.Eq(13 + 5 * vy, stones[0].y + 5 * stones[0].vy)
eq3a = sympy.Eq(10 + 5 * vz, stones[0].z + 5 * stones[0].vz)

# Second stone
eq1b = sympy.Eq(24 + 3 * vx, stones[1].x + 3 * stones[1].vx)
eq2b = sympy.Eq(13 + 3 * vy, stones[1].y + 3 * stones[1].vy)
eq3b = sympy.Eq(10 + 3 * vz, stones[1].z + 3 * stones[1].vz)

# Third stone
eq1c = sympy.Eq(24 + 4 * vx, stones[2].x + 4 * stones[2].vx)
eq2c = sympy.Eq(13 + 4 * vy, stones[2].y + 4 * stones[2].vy)
eq3c = sympy.Eq(10 + 4 * vz, stones[2].z + 4 * stones[2].vz)

sols = sympy.solve(
    [
        x + t1 * vx - (stones[0].x + t1 * stones[0].vx),
        y + t1 * vy - (stones[0].y + t1 * stones[0].vy),
        z + t1 * vz - (stones[0].z + t1 * stones[0].vz),
        x + t2 * vx - (stones[1].x + t2 * stones[1].vx),
        y + t2 * vy - (stones[1].y + t2 * stones[1].vy),
        z + t2 * vz - (stones[1].z + t2 * stones[1].vz),
        x + t3 * vx - (stones[2].x + t3 * stones[2].vx),
        y + t3 * vy - (stones[2].y + t3 * stones[2].vy),
        z + t3 * vz - (stones[2].z + t3 * stones[2].vz),
    ],
    dict=True,
)[0]

print(sols[x] + sols[y] + sols[z])
