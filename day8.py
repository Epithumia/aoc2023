from functools import reduce


def find_cycle(start: str) -> int:
    steps = 0
    current_node = start
    while current_node[-1] != "Z":
        current_node = network[current_node][instructions[steps % len(instructions)]]
        steps += 1
    return steps


def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)


def multi_lcm(*args):
    """Return lcm of args."""
    return reduce(lcm, args)


with open("input/input8.txt", "r") as f:
    data = f.read().splitlines()

instructions = data[0]
network = {row[0:3]: {"L": row[7:10], "R": row[-4:-1]} for row in data[2:]}

print("Partie 1 :", find_cycle('AAA'))

current_nodes = []
for k in network.keys():
    if k[-1] == "A":
        current_nodes.append(k)


print("Partie 2 :", multi_lcm(*[find_cycle(c) for c in current_nodes]))
