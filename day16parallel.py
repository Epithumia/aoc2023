import multiprocessing

with open("input/input16.txt", "r") as f:
    cave = [[c for c in r] for r in f.read().splitlines()]


def beam(start=(0, 0), start_direction="E"):
    class Tile:
        cave_map = {}
        X = len(cave)
        Y = len(cave[0])
        queue = list()

        def __init__(self, i, j, tile_type) -> None:
            self.i = i
            self.j = j
            self.tile_type = tile_type
            self.beams = {"N": False, "S": False, "E": False, "W": False}

        def shine(self, incoming):
            next_tiles = []
            directions = []
            if self.beams[incoming]:
                return None  # Light already passed this way
            if self.tile_type == ".":
                if incoming == "N":
                    next_tiles.append((self.i - 1, self.j))
                elif incoming == "S":
                    next_tiles.append((self.i + 1, self.j))
                elif incoming == "W":
                    next_tiles.append((self.i, self.j - 1))
                elif incoming == "E":
                    next_tiles.append((self.i, self.j + 1))
                self.beams[incoming] = True
                directions.append(incoming)
            elif self.tile_type == "-":
                if incoming == "N" or incoming == "S":
                    next_tiles.append((self.i, self.j + 1))
                    directions.append("E")
                    next_tiles.append((self.i, self.j - 1))
                    directions.append("W")
                    self.beams["E"] = True
                    self.beams["W"] = True
                    self.beams["N"] = True
                    self.beams["S"] = True
                elif incoming == "W":
                    next_tiles.append((self.i, self.j - 1))
                    directions.append(incoming)
                elif incoming == "E":
                    next_tiles.append((self.i, self.j + 1))
                    directions.append(incoming)
                self.beams[incoming] = True
            elif self.tile_type == "|":
                if incoming == "E" or incoming == "W":
                    next_tiles.append((self.i + 1, self.j))
                    directions.append("S")
                    next_tiles.append((self.i - 1, self.j))
                    directions.append("N")
                    self.beams["N"] = True
                    self.beams["S"] = True
                    self.beams["E"] = True
                    self.beams["W"] = True
                elif incoming == "N":
                    next_tiles.append((self.i - 1, self.j))
                    directions.append(incoming)
                elif incoming == "S":
                    next_tiles.append((self.i + 1, self.j))
                    directions.append(incoming)
                self.beams[incoming] = True
            elif self.tile_type == "/":
                if incoming == "N":
                    next_tiles.append((self.i, self.j + 1))
                    directions.append("E")
                elif incoming == "S":
                    next_tiles.append((self.i, self.j - 1))
                    directions.append("W")
                elif incoming == "W":
                    next_tiles.append((self.i + 1, self.j))
                    directions.append("S")
                elif incoming == "E":
                    next_tiles.append((self.i - 1, self.j))
                    directions.append("N")
                self.beams[incoming] = True
            else:  # "\"
                if incoming == "N":
                    next_tiles.append((self.i, self.j - 1))
                    directions.append("W")
                elif incoming == "S":
                    next_tiles.append((self.i, self.j + 1))
                    directions.append("E")
                elif incoming == "W":
                    next_tiles.append((self.i - 1, self.j))
                    directions.append("N")
                elif incoming == "E":
                    next_tiles.append((self.i + 1, self.j))
                    directions.append("S")
                self.beams[incoming] = True

            for i in range(len(next_tiles)):
                tile = next_tiles[i]
                if tile in self.cave_map:
                    self.queue.append((tile, directions[i]))

        @classmethod
        def process(cls):
            while len(cls.queue) > 0:
                (tile, direction) = cls.queue.pop()
                cls.cave_map[tile].shine(direction)

        @classmethod
        def reset(cls):
            for i in range(cls.X):
                for j in range(cls.Y):
                    cls.cave_map[(i, j)].beams = {
                        "N": False,
                        "S": False,
                        "E": False,
                        "W": False,
                    }

        def is_shining(self):
            if self.beams["N"] or self.beams["E"] or self.beams["S"] or self.beams["W"]:
                return True
            return False

    for r in range(len(cave)):
        for c in range(len(cave[r])):
            Tile.cave_map[(r, c)] = Tile(r, c, cave[r][c])

    Tile.cave_map[start].shine(start_direction)
    Tile.process()

    return sum([1 if Tile.cave_map[tile].is_shining() else 0 for tile in Tile.cave_map])


def partition(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


def multi_beam(vals):
    return max([beam(*val) for val in vals])


def run():
    print("Partie 1:", beam())

    X = len(cave)
    Y = len(cave[0])

    queue = []

    for j in range(Y):
        # Top row
        queue.append(((0, j), "S"))
        # Bottom row
        queue.append(((X - 1, j), "N"))
    for i in range(Y):
        # Left
        queue.append(((i, 0), "E"))
        # Right
        queue.append(((i, Y - 1), "W"))

    with multiprocessing.Pool(multiprocessing.cpu_count() - 1) as pool:
        results = pool.map(
            multi_beam, partition(queue, multiprocessing.cpu_count() - 1)
        )
    print("Partie 2:", max(results))


if __name__ == "__main__":
    run()
