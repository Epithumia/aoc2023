with open("input/input13.txt", "r") as f:
    data = f.read().split("\n\n")


def find_h_creases(plan, smudge=None):
    new_plan = [list(row) for row in plan]
    if smudge:
        new_plan[smudge[0]][smudge[1]] = (
            "." if new_plan[smudge[0]][smudge[1]] == "#" else "#"
        )
    pairs = []
    for i in range(len(new_plan) - 1):
        if new_plan[i] == new_plan[i + 1]:
            pairs.append((i, i + 1))
    return pairs


def check_h_fold(plan, pair, smudge=None):
    new_plan = [list(row) for row in plan]
    if smudge:
        new_plan[smudge[0]][smudge[1]] = (
            "." if new_plan[smudge[0]][smudge[1]] == "#" else "#"
        )
    top = len(new_plan)
    i = 0
    up, down = pair
    while up - i >= 0 and down + i < top:
        if not new_plan[up - i] == new_plan[down + i]:
            return False
        i += 1
    return True


def check_v_fold(plan, pair, smudge=None):
    new_plan = [list(row) for row in plan]
    if smudge:
        new_plan[smudge[0]][smudge[1]] = (
            "." if new_plan[smudge[0]][smudge[1]] == "#" else "#"
        )
    border = len(new_plan[0])
    i = 0
    left, right = pair
    while left - i >= 0 and right + i < border:
        if any(
            [
                new_plan[row][left - i] != new_plan[row][right + i]
                for row in range(len(new_plan))
            ]
        ):
            return False
        i += 1
    return True


def find_v_creases(plan, smudge=None):
    new_plan = [list(row) for row in plan]
    if smudge:
        new_plan[smudge[0]][smudge[1]] = (
            "." if new_plan[smudge[0]][smudge[1]] == "#" else "#"
        )
    pairs = []
    for i in range(len(new_plan[0]) - 1):
        if all(
            [new_plan[row][i] == new_plan[row][i + 1] for row in range(len(new_plan))]
        ):
            pairs.append((i, i + 1))
    return pairs


maps = []
for row in data:
    maps.append(row.splitlines())


def smudge_v(plan, pairs):
    for i in range(len(plan)):
        for j in range(len(plan[0])):
            creases = find_v_creases(plan, (i, j))
            for crease in creases:
                if crease not in pairs and check_v_fold(plan, crease, (i, j)):
                    return crease[1]
    return 0


def smudge_h(plan, pairs):
    for i in range(len(plan)):
        for j in range(len(plan[0])):
            creases = find_h_creases(plan, (i, j))
            for crease in creases:
                if crease not in pairs and check_h_fold(plan, crease, (i, j)):
                    return crease[1]
    return 0


nb_rows = 0
nb_rows_p2 = 0
nb_cols = 0
nb_cols_p2 = 0
for plan in maps:
    pairs = []
    creases = find_v_creases(plan)
    for crease in creases:
        if check_v_fold(plan, crease):
            pairs.append(crease)
            nb_cols += crease[1]
    nb_cols_p2 += smudge_v(plan, pairs)

    pairs = []
    creases = find_h_creases(plan)
    for crease in creases:
        if check_h_fold(plan, crease):
            pairs.append(crease)
            nb_rows += crease[1]
    nb_rows_p2 += smudge_h(plan, pairs)


print("Partie 1:", nb_cols + nb_rows * 100)
print("Partie 2:", nb_cols_p2 + nb_rows_p2 * 100)
