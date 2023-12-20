from typing import Dict
import portion as P

with open("input/input19.txt", "r") as f:
    data = f.read().split("\n\n")


class Rule:
    def __init__(self, check, effect) -> None:
        self.effect = effect
        if check is None:
            self.rating = None
            self.threshold = None
            self.mode = None
        else:
            self.rating = check[0]
            self.mode = check[1]
            self.threshold = int(check[2:])

    def apply(self, part):
        if self.mode is None:
            return self.effect
        if self.mode == "<":
            if part[self.rating] < self.threshold:
                return self.effect
        else:
            if part[self.rating] > self.threshold:
                return self.effect
        return False

    def predict(self, part: Dict[str, P.Interval]):
        if self.mode is None:
            return [(self.effect, part)]
        part_a = part.copy()
        part_b = part

        if self.mode == "<":
            part_a[self.rating] = part_a[self.rating].intersection(
                P.closed(0, self.threshold - 1)
            )
            part_b[self.rating] = part_b[self.rating].intersection(
                P.closed(self.threshold, 4000)
            )
            return [(self.effect, part_a), (False, part_b)]
        else:
            part_a[self.rating] = part_a[self.rating].intersection(
                P.closed(0, self.threshold)
            )
            part_b[self.rating] = part_b[self.rating].intersection(
                P.closed(self.threshold + 1, 4000)
            )
            return [(False, part_a), (self.effect, part_b)]


parts = []
for row in data[1].splitlines():
    p = row[1:-1].split(",")
    x = int(p[0].split("=")[1])
    m = int(p[1].split("=")[1])
    a = int(p[2].split("=")[1])
    s = int(p[3].split("=")[1])
    parts.append({"x": x, "m": m, "a": a, "s": s})

workflows = {}

for row in data[0].splitlines():
    name = row.split("{")[0]
    rule_set = row.split(name)[1][1:-1].split(",")
    rules = []
    for r in rule_set:
        r = r.split(":")
        if len(r) == 2:
            rules.append(Rule(r[0], r[1]))
        else:
            rules.append(Rule(None, r[0]))
    workflows[name] = rules

score = 0
for part in parts:
    cur = "in"
    i = 0
    result = workflows[cur][i].apply(part)
    while result not in ["A", "R"]:
        if not result:  # Same workflow, next test
            i += 1
            result = workflows[cur][i].apply(part)
        else:
            i = 0
            cur = result
            result = workflows[cur][i].apply(part)
    if result == "A":
        score += part["x"] + part["m"] + part["a"] + part["s"]

print("Partie 1:", score)

queue = [
    (
        "in",
        {
            "x": P.closed(1, 4000),
            "m": P.closed(1, 4000),
            "a": P.closed(1, 4000),
            "s": P.closed(1, 4000),
        },
        0,
    )
]
accept = []
while len(queue) > 0:
    op = queue.pop()
    if op[0] == "A":
        accept.append(op[1])
    elif op[0] != "R":
        results = workflows[op[0]][op[2]].predict(op[1])
        for res in results:
            if res[0] == False:
                queue.append((op[0], res[1], op[2] + 1))
            else:
                queue.append((res[0], res[1], 0))

total_score = 0
for part in accept:
    x = part["x"].upper - part["x"].lower + 1
    m = part["m"].upper - part["m"].lower + 1
    a = part["a"].upper - part["a"].lower + 1
    s = part["s"].upper - part["s"].lower + 1
    score = x * m * a * s
    total_score += score

print("Partie 2:", total_score)
