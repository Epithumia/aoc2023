from functools import lru_cache

with open("input/input12.txt", "r") as f:
    springs = f.read().splitlines()


@lru_cache(maxsize=None)
def count_arrangements(data: str, code: str):
    nb = 0
    if len(code) == 0:
        if "#" in data or len(data) == 0:
            return 0
        else:
            if len(data) > 0:
                return 1
            return 0
    list_code = [int(x) for x in code.split(",")]
    prepared = data.strip(".")
    if len(list_code) > 0 and len(prepared) < list_code[0]:
        return 0
    if len(prepared) == 0:
        if len(code) == 0:
            return 0
        return 0
    if len(prepared) == 1:
        if len(code) == 0 and prepared[0] == "#":
            return 0
        if len(code) == 0 and prepared[0] != "#":
            print("hit b:", data, code)
            return 1
        if len(code) > 1:
            return 0
    if prepared[0] == "?":
        x = count_arrangements("." + prepared[1:], code)
        y = count_arrangements("#" + prepared[1:], code)
        return x + y
    if prepared[0] == "#":
        candidate = prepared[0 : list_code[0]]
        if "." in candidate:
            return 0
        if (
            len(list_code) == 1
            and len(prepared) == list_code[0]
            and "." not in prepared
        ):
            return 1
        if len(prepared) > list_code[0] and prepared[list_code[0]] == "#":
            return 0
        x = count_arrangements(
            "." + prepared[list_code[0] + 1 :],
            ",".join([str(x) for x in list_code[1:]]),
        )
        return x
    return nb


def unfold(spring):
    s = spring.split()
    return (
        s[0]
        + "?"
        + s[0]
        + "?"
        + s[0]
        + "?"
        + s[0]
        + "?"
        + s[0]
        + " "
        + s[1]
        + ","
        + s[1]
        + ","
        + s[1]
        + ","
        + s[1]
        + ","
        + s[1]
    )


m = 0
for spring in springs:
    sp = spring.split()
    data = sp[0]
    code = sp[1]
    c = count_arrangements(data, code)
    m += c
print(m)

m = 0
for spring in springs:
    sp = unfold(spring).split()
    data = sp[0]
    code = sp[1]
    c = count_arrangements(data, code)
    m += c
print(m)
