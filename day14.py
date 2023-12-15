with open("input/input14.txt", "r") as f:
    plan = f.read().splitlines()


def tilt(plan: list, direction="N") -> list:
    tilted = [list(row) for row in plan]
    if direction in ("N", "S"):
        for col in range(len(tilted[0])):
            column = []
            for row in range(len(tilted)):
                column.append(tilted[row][col])
            column = "#".join(
                [
                    "".join(sorted(bit, reverse=(direction == "N")))
                    for bit in "".join(column).split("#")
                ]
            )
            for row in range(len(tilted)):
                tilted[row][col] = column[row]
    if direction in ("E", "W"):
        for row in range(len(tilted)):
            tilted[row] = list(
                "#".join(
                    [
                        "".join(sorted(bit, reverse=(direction == "W")))
                        for bit in "".join(tilted[row]).split("#")
                    ]
                )
            )
    return tilted


def weight(plan):
    total = 0
    weight = len(plan)
    i = 1
    while weight > 0:
        total += sum([1 if c == "O" else 0 for c in plan[i - 1]]) * weight
        i += 1
        weight -= 1
    return total


def cycle(plan):
    plan = tilt(plan, "N")
    plan = tilt(plan, "W")
    plan = tilt(plan, "S")
    plan = tilt(plan, "E")
    return plan


def find_cycle_length(ctrl):
    ctrl_str = ",".join(ctrl)
    checks = []
    for i in range(len(ctrl)):
        sub = ",".join(ctrl[-(i + 1) :])
        checks.append(ctrl_str.count(sub))
        if 2 * ctrl_str.count(sub) in checks:
            return i
    return -1


def find_non_cycle_length(ctrl, cycle_length):
    i = 0
    ctrl_str = ",".join(ctrl)
    while i + cycle_length < len(ctrl):
        sub = ",".join(ctrl[i : i + cycle_length])
        if ctrl_str.count(sub) > 1:
            return i
        i += 1
    return -1


tilted = tilt(plan)

print("Partie 1:", weight(tilted))

seen = []
cycled = cycle(plan)
x = "".join(["".join(row) for row in cycled])
while x not in seen:
    seen.append(x)
    cycled = cycle(cycled)
    x = "".join(["".join(row) for row in cycled])

s = seen.index(x)
c = len(seen) - s

for _ in range((1000000000 - s) % c - 1):
    cycled = cycle(cycled)

print("Partie 2:", weight(cycled))
