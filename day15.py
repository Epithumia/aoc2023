from collections import defaultdict


def hash_code(word):
    hash_value = 0
    for c in word:
        hash_value += ord(c)
        hash_value *= 17
        hash_value = hash_value % 256
    return hash_value


def focusing_power(box):
    i = 1
    fp = 0
    for key in box.keys():
        fp += i * int(box[key])
        i += 1
    return fp


with open("input/input15.txt", "r") as f:
    data = f.read().splitlines()

sequence = data[0].split(",")

print("Partie 1:", sum([hash_code(word) for word in sequence]))

boxes = defaultdict(lambda: dict())

for word in sequence:
    if "=" in word:
        label = word.split("=")[0]
        target = hash_code(label)
        boxes[target][label] = word[-1]
    else:
        label = word[:-1]
        target = hash_code(label)
        if label in boxes[target]:
            boxes[target].pop(label)

total_power = 0

for i in range(256):
    total_power += (i + 1) * focusing_power(boxes[i])

print("Partie 2:", total_power)
