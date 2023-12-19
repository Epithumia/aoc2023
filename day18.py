import shapely

with open("input/input18.txt", "r") as f:
    data = f.read().splitlines()


coords = [(0, 0)]
i = j = 0
for row in data:
    r = row.split()
    direction = r[0]
    length = int(r[1])
    if direction == "R":
        i += length
    elif direction == "D":
        j -= length
    elif direction == "L":
        i -= length
    else:
        j += length
    coords.append((i, j))

polygon = shapely.Polygon(coords)
p2 = polygon.buffer(1, join_style=2)
print("Partie 1:", int((polygon.area + p2.area) // 2 - 1))

coords = [(0, 0)]
i = j = 0
for row in data:
    r = row.split()
    code = r[2][2:-1]
    length = int(code[0:-1], 16)
    if code[-1] == "0":
        direction = "R"
        i += length
    elif code[-1] == "1":
        direction = "D"
        j -= length
    elif code[-1] == "2":
        direction = "L"
        i -= length
    else:
        direction = "U"
        j += length
    coords.append((i, j))

polygon = shapely.Polygon(coords)
p2 = polygon.buffer(1, join_style=2)
print("Partie 2:", int((polygon.area + p2.area) // 2 - 1))
