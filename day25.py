from collections import defaultdict
from ortools.sat.python import cp_model

with open("input/input25.txt", "r") as f:
    data = f.read().splitlines()

vertices = defaultdict()
edges = defaultdict()

part1 = cp_model.CpModel()

for row in data:
    left = row.split(":")[0]
    right = row.split(":")[1].split()
    vertices[left] = part1.NewIntVar(0, 1, left)
    for node in right:
        vertices[node] = part1.NewIntVar(0, 1, node)
        if node + "_" + left not in edges:
            edges[left + "_" + node] = part1.NewBoolVar(node)

for edge in edges:
    left = edge[0:3]
    right = edge[4:]
    part1.Add(vertices[left] != vertices[right]).OnlyEnforceIf(edges[edge])
    part1.Add(vertices[left] == vertices[right]).OnlyEnforceIf(edges[edge].Not())

part1.AddLinearConstraint(sum([edges[e] for e in edges]), 3, 3)

solver = cp_model.CpSolver()
status = solver.Solve(part1)

left = 0
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    for v in vertices:
        left += solver.Value(vertices[v])

    print("Partie 1:", left * (len(vertices) - left))
