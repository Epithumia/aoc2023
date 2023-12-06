with open("input/input3.txt", "r") as f:
    data = f.read().splitlines()


def find_parts(numbers, symbols):
    parts = []
    gears = []

    potential_gears = {}

    for n in numbers.keys():
        number = list(numbers[n].keys())[0]
        positions = numbers[n][number]
        seen = False
        for r, c in positions:
            for x, y in [
                (r - 1, c - 1),
                (r - 1, c),
                (r - 1, c + 1),
                (r, c - 1),
                (r, c + 1),
                (r + 1, c - 1),
                (r + 1, c),
                (r + 1, c + 1),
            ]:
                if (x, y) in symbols:
                    if not seen:
                        parts.append(number)
                        seen = True
                if (x, y) in symbols and symbols[(x, y)] == "*":
                    if (x, y) not in potential_gears:
                        potential_gears[(x, y)] = []
                    if n not in potential_gears[(x, y)]:
                        potential_gears[(x, y)].append(n)

    for gear in potential_gears.keys():
        if len(potential_gears[gear]) == 2:
            gears.append(potential_gears[gear])

    return parts, gears


symbols = {}
numbers = {}
num = ""
pos = []
for r in range(len(data)):
    if num != "":
        numbers[pos[0]] = {int(num): pos[:]}
        pos = []
        num = ""
    row = data[r]
    for c in range(len(row)):
        if not str.isdigit(l := row[c]) and l != ".":
            if num != "":
                numbers[pos[0]] = {int(num): pos[:]}
                pos = []
                num = ""
            symbols[(r, c)] = l
        elif l == ".":
            if num != "":
                numbers[pos[0]] = {int(num): pos[:]}
                pos = []
                num = ""
        elif l != ".":
            num += l
            pos.append((r, c))

parts, gears = find_parts(numbers, symbols)
print("Partie 1 :", sum(parts))
print(
    "Partie 2 :",
    sum([list(numbers[g[0]].keys())[0] * list(numbers[g[1]].keys())[0] for g in gears]),
)
