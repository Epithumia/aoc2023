from collections import defaultdict, deque

def find_next_crossing(start, next):
    trail = [start, next]
    check = True
    while check:
        check = False
        pos = trail[-1]
        neighbors = []
        potential_neighbors = [(pos[0]-1, pos[1]), (pos[0]+1, pos[1]), (pos[0], pos[1]-1), (pos[0], pos[1]+1)]
        for pot in potential_neighbors:
            if trail_map_dict[pot] != "#" and pot not in trail:
                neighbors.append(pot)
        if len(neighbors) == 1:
            trail.append(neighbors[0])
            check = True
        if len(neighbors) > 1:
            return (pos, len(trail) - 1)
    return None, None

def x_neighbors(node, compact_map):
    neighbors = []
    for (s, e) in compact_map.keys():
        if node == s:
            neighbors.append(e)
    return neighbors

def trail_len(trail):
    if trail is None:
        return 0
    l = 0
    for i in range(len(trail) - 1):
        l += compact_map[trail[i], trail[i+1]]
    return l

with open('input/input23.txt', 'r') as f:
    data = f.read().splitlines()

trail_map = [[c for c in row] for row in data]
trail_map_dict = defaultdict(lambda: "#")
for i in range(len(trail_map)):
    for j in range(len(trail_map[0])):
        trail_map_dict[i,j] = trail_map[i][j]

start = (0, 1)
end = (len(trail_map)-1, len(trail_map[0]) - 2)
best_trail = []
queue = deque()
queue.append([start])

while len(queue) > 0:
    # Get current path
    trail = queue.pop()
    # Get current position
    pos = trail[-1]
    if pos == end and len(trail) > len(best_trail):
        best_trail = trail[:]
        #break
    else:
        # Get the four neighbors
        neighbors = [(pos[0]-1, pos[1]), (pos[0]+1, pos[1]), (pos[0], pos[1]-1), (pos[0], pos[1]+1)]
        if trail_map_dict[pos] == ">" and neighbors[3] not in trail:
            trail.append(neighbors[3])
            queue.append(trail)
        elif trail_map_dict[pos] == "<" and neighbors[2] not in trail:
            trail.append(neighbors[2])
            queue.append(trail)
        elif trail_map_dict[pos] == "^" and neighbors[0] not in trail:
            trail.append(neighbors[0])
            queue.append(trail)
        elif trail_map_dict[pos] == "v" and neighbors[1] not in trail:
            trail.append(neighbors[1])
            queue.append(trail)
        elif trail_map_dict[pos] == ".":
            for n in neighbors:
                if trail_map_dict[n] != "#" and n not in trail:
                    t = trail[:]
                    t.append(n)
                    queue.append(t)

print("Partie 1:", len(best_trail) - 1)


# compress map
compact_map = {}
queue.append((start, (start[0]+1, start[1])))
queue.append((end, (end[0]-1, end[1])))
seen = []
while len(queue) > 0:
    current, next = queue.popleft()
    seen.append((current, next))
    node, dist = find_next_crossing(current, next)
    if node is not None:
        if (current, node) not in compact_map:
            compact_map[current, node] = dist
        else:
            compact_map[current, node] = max(compact_map[current, node], dist)
        compact_map[node, current] = compact_map[current, node]
        potential_neighbors = [(node[0]-1, node[1]), (node[0]+1, node[1]), (node[0], node[1]-1), (node[0], node[1]+1)]
        for pot in potential_neighbors:
            if trail_map_dict[pot] != "#" and (node, pot) not in seen:
                queue.append((node, pot))


best_trail = None
queue.append([start])
while len(queue) > 0:
    # Get current path
    trail = queue.pop()
    # Get current position
    pos = trail[-1]
    if pos == end and trail_len(trail) > trail_len(best_trail):
        best_trail = trail[:]
    else:
        neighbors = x_neighbors(pos, compact_map)
        for n in neighbors:
            if n not in trail:
                t = trail[:]
                t.append(n)
                queue.append(t)

print("Partie 2:", trail_len(best_trail))