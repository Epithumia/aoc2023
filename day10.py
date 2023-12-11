with open("input/input10.txt", "r") as f:
    data = [[cell for cell in row] for row in f.read().splitlines()]


class Cell:
    def __init__(self, i: int, j: int, shape: str) -> None:
        self.cell_a = None
        self.cell_b = None
        self.i = i
        self.j = j
        self.shape = shape
        self.visited = False

    def link(self, cell_a, cell_b) -> None:
        self.cell_a = cell_a
        self.cell_b = cell_b
        if cell_a is not None and cell_a.shape == "S":
            cell_a.link_start(self)
        if cell_b is not None and cell_b.shape == "S":
            cell_b.link_start(self)

    def link_start(self, cell):
        if self.cell_a is None:
            self.cell_a = cell
        else:
            self.cell_b = cell

    def move(self, origin):
        if origin == self.cell_a:
            return self.cell_b
        else:
            return self.cell_a

    def map_neighbors(self):
        if self.shape == "|":
            return [(self.i - 1, self.j), (self.i + 1, self.j)]
        if self.shape == "-":
            return [(self.i, self.j - 1), (self.i, self.j + 1)]
        if self.shape == "L":
            return [(self.i - 1, self.j), (self.i, self.j + 1)]
        if self.shape == "J":
            return [(self.i - 1, self.j), (self.i, self.j - 1)]
        if self.shape == "7":
            return [(self.i + 1, self.j), (self.i, self.j - 1)]
        if self.shape == "F":
            return [(self.i + 1, self.j), (self.i, self.j + 1)]
        return None

    def __repr__(self) -> str:
        return f"{self.i},{self.j} [{self.shape}] neighbors: {(self.cell_a is not None) + (self.cell_b is not None)}"


def color(pipe_map, cell_a, cell_b, cell_c):
    if cell_a.i == cell_b.i - 1:
        # Down
        if cell_b.i == cell_c.i - 1:
            # Down, down
            if cell_b.j > 0 and not pipe_map[cell_b.i][cell_b.j - 1].visited:
                pipe_map[cell_b.i][cell_b.j - 1].visited = True
                pipe_map[cell_b.i][cell_b.j - 1].shape = "1"
        elif cell_b.j == cell_c.j - 1:
            # Down, left
            if cell_b.j > 0 and not pipe_map[cell_b.i][cell_b.j - 1].visited:
                pipe_map[cell_b.i][cell_b.j - 1].visited = True
                pipe_map[cell_b.i][cell_b.j - 1].shape = "1"
            if (
                cell_b.i < len(pipe_map) - 1
                and not pipe_map[cell_b.i + 1][cell_b.j].visited
            ):
                pipe_map[cell_b.i + 1][cell_b.j].visited = True
                pipe_map[cell_b.i + 1][cell_b.j].shape = "1"
        else:
            # Down, right
            if not pipe_map[cell_a.i][cell_c.j].visited:
                pipe_map[cell_a.i][cell_c.j].visited = True
                pipe_map[cell_a.i][cell_c.j].shape = "1"
    elif cell_a.i == cell_b.i + 1:
        # Up
        if cell_b.i == cell_c.i + 1:
            # Up, up
            if (
                cell_b.j < len(pipe_map[0]) - 1
                and not pipe_map[cell_b.i][cell_b.j + 1].visited
            ):
                pipe_map[cell_b.i][cell_b.j + 1].visited = True
                pipe_map[cell_b.i][cell_b.j + 1].shape = "1"
        elif cell_b.j == cell_c.j + 1:
            # Up, left
            if cell_b.i > 0 and not pipe_map[cell_b.i - 1][cell_b.j].visited:
                pipe_map[cell_b.i - 1][cell_b.j].visited = True
                pipe_map[cell_b.i - 1][cell_b.j].shape = "1"
            if (
                cell_b.j < len(pipe_map[0]) - 1
                and not pipe_map[cell_b.i][cell_b.j + 1].visited
            ):
                pipe_map[cell_b.i][cell_b.j + 1].visited = True
                pipe_map[cell_b.i][cell_b.j + 1].shape = "1"
        else:
            # Up, right
            if not pipe_map[cell_c.i][cell_a.j].visited:
                pipe_map[cell_c.i][cell_a.j].visited = True
                pipe_map[cell_c.i][cell_a.j].shape = "1"
    elif cell_a.j == cell_b.j - 1:
        # Right
        if cell_b.j == cell_c.j - 1:
            # Right, right
            if not pipe_map[cell_b.i][cell_b.j + 1].visited:
                pipe_map[cell_b.i][cell_b.j + 1].visited = True
                pipe_map[cell_b.i][cell_b.j + 1].shape = "1"
        elif cell_b.i == cell_c.i - 1:
            # Right, down
            if not pipe_map[cell_a.i][cell_c.j].visited:
                pipe_map[cell_a.i][cell_c.j].visited = True
                pipe_map[cell_a.i][cell_c.j].shape = "1"
        else:
            # Right, up
            if (
                cell_b.j < len(pipe_map[0]) - 1
                and not pipe_map[cell_b.i][cell_b.j + 1].visited
            ):
                pipe_map[cell_b.i][cell_b.j + 1].visited = True
                pipe_map[cell_b.i][cell_b.j + 1].shape = "1"
            if (
                cell_b.i < len(pipe_map) - 1
                and not pipe_map[cell_b.i + 1][cell_b.j].visited
            ):
                pipe_map[cell_b.i + 1][cell_b.j].visited = True
                pipe_map[cell_b.i + 1][cell_b.j].shape = "1"
    else:
        # Left
        if cell_b.j == cell_c.j + 1:
            # Left, left
            if not pipe_map[cell_b.i][cell_b.j - 1].visited:
                pipe_map[cell_b.i][cell_b.j - 1].visited = True
                pipe_map[cell_b.i][cell_b.j - 1].shape = "1"
        elif cell_b.i == cell_c.i + 1:
            # Left, up
            if not pipe_map[cell_c.i][cell_a.j].visited:
                pipe_map[cell_c.i][cell_a.j].visited = True
                pipe_map[cell_c.i][cell_a.j].shape = "1"
        else:
            # left, down
            if cell_b.i > 0 and not pipe_map[cell_b.i - 1][cell_b.j].visited:
                pipe_map[cell_b.i - 1][cell_b.j].visited = True
                pipe_map[cell_b.i - 1][cell_b.j].shape = "1"
            if cell_b.j > 0 and not pipe_map[cell_b.i][cell_b.j - 1].visited:
                pipe_map[cell_b.i][cell_b.j - 1].visited = True
                pipe_map[cell_b.i][cell_b.j - 1].shape = "1"


def flood(pipe_map):
    queue = []
    for row in pipe_map:
        for cell in row:
            if cell.shape == "1":
                queue.append(cell)
    while len(queue) > 0:
        cell = queue.pop(0)
        if not cell.visited:
            cell.visited = True
            cell.shape = "1"
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                ni = cell.i + i
                nj = cell.j + j
                if (
                    (0 <= ni < len(pipe_map))
                    and (0 <= nj < len(pipe_map[0]))
                    and (not pipe_map[ni][nj].visited)
                    and (pipe_map[ni][nj] not in queue)
                ):
                    queue.append(pipe_map[ni][nj])


pipe_map = []

for row in range(len(data)):
    r = data[row]
    map_row = []
    for col in range(len(r)):
        c = r[col]
        cell = Cell(row, col, c)
        if c == "S":
            start = (row, col)
        map_row.append(cell)
    pipe_map.append(map_row)

for row in range(len(pipe_map)):
    r = pipe_map[row]
    for col in range(len(r)):
        c = r[col]
        neighbors = c.map_neighbors()
        if neighbors:
            n1 = None
            n2 = None
            try:
                n1 = pipe_map[neighbors[0][0]][neighbors[0][1]]
            except IndexError:
                pass
            try:
                n2 = pipe_map[neighbors[1][0]][neighbors[1][1]]
            except IndexError:
                pass
            c.link(n1, n2)

distance = 1
previous = pipe_map[start[0]][start[1]]
previous.visited = True
current = previous.cell_a

while current.shape != "S":
    next_cell = current.move(previous)
    previous = current
    previous.visited = True
    current = next_cell
    distance += 1

print("Partie 1 :", distance // 2)

previous = pipe_map[start[0]][start[1]]
current = previous.cell_a

while current.shape != "S":
    next_cell = current.move(previous)
    color(pipe_map, previous, current, next_cell)
    previous = current
    current = next_cell

flood(pipe_map)

zeroes = sum([sum([1 if not cell.visited else 0 for cell in row]) for row in pipe_map])

print("Partie 2 :", zeroes)
