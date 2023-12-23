from typing import List


class Block():
    def __init__(self, coords, id) -> None:
        d = coords.split("~")
        start = d[0].split(",")
        end = d[1].split(",")
        self.x_start = min(int(start[0]), int(end[0]))
        self.x_end = max(int(start[0]), int(end[0]))
        self.y_start = min(int(start[1]), int(end[1]))
        self.y_end = max(int(start[1]), int(end[1]))
        self.z_start = min(int(start[2]), int(end[2]))
        self.z_end = max(int(start[2]), int(end[2]))
        self.id = id

    def __lt__(self, other):
        if self.z_start < other.z_start:
            return True
        if self.z_start > other.z_start:
            return False
        if self.x_start < other.x_start:
            return True
        if self.x_start > other.x_start:
            return False
        if self.y_start < other.y_start:
            return True
        if self.y_start > other.y_start:
            return False
        return False
    
    def __str__(self) -> str:
        return f"{self.id}: {self.x_start},{self.y_start},{self.z_start}-{self.x_end},{self.y_end},{self.z_end}"
    
    def __repr__(self) -> str:
        return f"{self.id}: {self.x_start},{self.y_start},{self.z_start}-{self.x_end},{self.y_end},{self.z_end}"

    def supports(self, bricks):
        # Chercher les briques dont le zstart est self.zend+1 et dont self(x,y) est dans slice z+1
        support_bricks = []
        for brick in slice(bricks, self.z_end + 1):
            if brick.z_start == self.z_end + 1:
                if any([(self.x_start <= x <= self.x_end) and self.y_start <= y <= self.y_end for x in range(brick.x_start, brick.x_end + 1) for y in range(brick.y_start, brick.y_end + 1)]):
                    support_bricks.append(brick)
        return support_bricks

    def rests_on(self, blocks):
        # Prendre le code qui permet de savoir si on peut descendre et modifier pour renvoyer une liste de briques
        rests = []
        block_slice = slice(blocks, self.z_start-1)
        if len(block_slice) == 0:
            return []
        for block in block_slice:
            if any([(self.x_start <= x <= self.x_end) and (self.y_start <= y <= self.y_end) for x in range(block.x_start, block.x_end + 1) for y in range(block.y_start, block.y_end + 1)]) and block.z_end == self.z_start - 1:
                rests.append(block)
        return rests

def slice(blocks, z) -> List[Block]:
    sliced_blocks = []
    for block in blocks:
        if block.z_start <= z <= block.z_end:
            sliced_blocks.append(block)
    return sliced_blocks

def xy_slice(blocks, z):
    coords = []
    for block in blocks:
        if block.z_start <= z <= block.z_end:
            for x in range(block.x_start, block.x_end + 1):
                for y in range(block.y_start, block.y_end + 1):
                    coords.append((x,y))
    return coords


with open('input/input22.txt', 'r') as f:
    data = f.read().splitlines()

blocks = []
i=1
for row in data:
    blocks.append(Block(row, i))
    # print(Block(row, i), row)
    i += 1

blocks.sort()

has_moved = True
while has_moved:
    has_moved = False
    for block in blocks:
        z = block.z_start
        block_slice = xy_slice(blocks, z-1)
        if z == 1:
            continue
        if len(block_slice) == 0:
            block.z_start -= 1
            block.z_end -= 1
            has_moved = True
            continue
        if not any([(x, y) in block_slice for x in range(block.x_start, block.x_end + 1) for y in range(block.y_start, block.y_end + 1)]):
            block.z_start -= 1
            block.z_end -= 1
            has_moved = True
            continue

blocks.sort()

safe_blocks = []
fall_potential = {}

for block in blocks:
    if not any([len(b.rests_on(blocks)) == 1 for b in block.supports(blocks)]):
        safe_blocks.append(block)
        fall_potential[(block,)] = 0

print("Partie 1:", len(safe_blocks))

total = 0
for i in range(len(blocks)):
    falling = set()
    block = blocks[len(blocks)-i-1]
    if (block,) not in safe_blocks:  # Block is not safe to disintegrate
        queue = [block]
        falling.add(block)
        while len(queue) > 0:
            block = queue.pop()
            carried = block.supports(blocks)
            for carried_block in carried:  # Check if other blocks support this one
                carriers = carried_block.rests_on(blocks)
                if all([carrier in falling for carrier in carriers]):
                    falling.add(carried_block)
                    queue.append(carried_block)
    total += len(falling)-1

print("Partie 2:", total)