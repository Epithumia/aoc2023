with open("input/input5.txt", "r") as f:
    data = f.read()


def process(val, key):
    process_map = maps[key]
    for low, high in process_map.keys():
        if low <= val < high:
            return val + process_map[(low, high)]
    return val


def plant(seed):
    # seed-to-soil
    soil = process(seed, "seed-to-soil")
    # soil-to-fertilizer
    fertilizer = process(soil, "soil-to-fertilizer")
    # fertilizer-to-water
    water = process(fertilizer, "fertilizer-to-water")
    # water-to-light
    light = process(water, "water-to-light")
    # light-to-temperature
    temp = process(light, "light-to-temperature")
    # temperature-to-humidity
    humidity = process(temp, "temperature-to-humidity")
    # humidity-to-location
    location = process(humidity, "humidity-to-location")
    return location


def find_true_map():
    deltas = {}
    while len(queue) > 0:
        start, mid = queue.pop()
        end = mid
        delta1 = plant(start) - start
        delta2 = plant(mid) - mid

        while delta1 != delta2:
            mid = (start + mid) // 2
            delta1 = plant(start) - start
            delta2 = plant(mid) - mid

        deltas[(start, mid)] = delta1
        if mid + 1 < end:
            queue.append((mid + 1, end))

    return deltas


seeds = [int(x) for x in data.splitlines()[0].split()[1:]]

premaps = {
    row.split(":\n")[0].replace(" map", ""): [
        line.splitlines() for line in row.split(":\n")[1:]
    ][0]
    for row in data.split("\n\n")[1:]
}
maps = {}
for key in premaps.keys():
    maps[key] = {}
    for row in premaps[key]:
        tri = row.split()
        dest, orig, ran = int(tri[0]), int(tri[1]), int(tri[2])
        maps[key][(orig, orig + ran)] = dest - orig
    maps[key] = dict(sorted(maps[key].items()))

closest = 2**32 - 1

for seed in seeds:
    pos = plant(seed)
    if pos < closest:
        closest = pos

print(closest)

queue = []
seed_ranges = []
for i in range(len(seeds) // 2):
    seed_ranges.append((seeds[2 * i], seeds[2 * i + 1]))

seed_ranges.sort()

for pair in seed_ranges:
    queue.append((pair[0], pair[0] + pair[1]))

deltas = find_true_map()

minimum = 2**32 - 1
for k in deltas.keys():
    if k[0] + deltas[k] < minimum:
        minimum = k[0] + deltas[k]

print(minimum)
