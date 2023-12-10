with open("input/input9.txt", "r") as f:
    data = f.read().splitlines()


def extrapolate(hist: list[int], backwards=False):
    current = hist[:]
    stack = []
    while any([x != 0 for x in current]):
        reduced = []
        for i in range(len(current) - 1):
            reduced.append(current[i + 1] - current[i])
        stack.append(reduced[:])
        current = reduced[:]
    current = stack.pop()
    if not backwards:
        last = current[-1]
        while len(stack) > 0:
            current = stack.pop()
            last = current[-1] + last
        return hist[-1] + last
    else:
        first = current[0]
        while len(stack) > 0:
            current = stack.pop()
            first = current[0] - first
        return hist[0] - first


sequences = [[int(x) for x in row.split()] for row in data]

print("Partie 1 :", sum([extrapolate(hist) for hist in sequences]))
print("Partie 2 :", sum([extrapolate(hist, True) for hist in sequences]))
