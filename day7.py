from collections import defaultdict


with open("input/input7.txt", "r") as f:
    data = f.read().splitlines()


def hand_type(hand: str, simple=True) -> str:
    hand_conversion = {
        "5": "A",
        "41": "B",
        "32": "C",
        "311": "D",
        "221": "E",
        "2111": "F",
        "11111": "G",
    }
    cards = [c for c in hand]
    s = defaultdict(lambda: 0)
    for card in cards:
        s[card] += 1
    t = []
    j = 0
    for e in s:
        if simple or (not simple and e != "J"):
            t.append(s[e])
        else:
            j += s[e]
    if len(t) == 0:
        t.append(0)
    t.sort(reverse=True)
    t[0] += j
    hand_code = "".join([str(c) for c in t])
    return hand_conversion[hand_code]


def recode_hand(hand: str, simple=True) -> str:
    translation = {
        "A": "A",
        "K": "B",
        "Q": "C",
        "J": "D",
        "T": "E",
        "9": "F",
        "8": "G",
        "7": "H",
        "6": "I",
        "5": "J",
        "4": "K",
        "3": "L",
        "2": "M",
    }
    if not simple:
        translation["J"] = "N"
    return "".join([translation[c] for c in hand])


hands = {}
coded_hands = []
joker_coded_hands = []
decode = {}
joker_decode = {}
for row in data:
    r = row.split()
    hands[r[0]] = int(r[1])
    coded_hand = hand_type(r[0]) + recode_hand(r[0])
    joker_coded_hand = hand_type(r[0], False) + recode_hand(r[0], False)
    decode[coded_hand] = r[0]
    joker_decode[joker_coded_hand] = r[0]
    coded_hands.append(coded_hand)
    joker_coded_hands.append(joker_coded_hand)

coded_hands.sort(reverse=True)
joker_coded_hands.sort(reverse=True)

winnings = 0
joker_winnings = 0
for i in range(len(coded_hands)):
    winnings += (i + 1) * hands[decode[coded_hands[i]]]
    joker_winnings += (i + 1) * hands[joker_decode[joker_coded_hands[i]]]

print("Partie 1:", winnings)

print("Partie 2:", joker_winnings)
