with open("input/input4.txt", "r") as f:
    data = f.read().splitlines()

cards = {}
score1 = 0
score2 = 0

for row in data:
    r = row.split(":")
    card = int(r[0].split(" ")[-1].strip())
    n = r[1].split("|")
    winning = set([int(x) for x in " ".join(n[0].split()).split(" ")])
    numbers = set([int(x) for x in " ".join(n[-1].split()).split(" ")])
    correct = winning.intersection(numbers)
    sc = 2**(len(correct)-1)
    if sc < 1:
        sc = 0
    score1 += sc
    cards[card] = {'match': len(correct), 'quantity': 1}

print("Partie 1 :", score1)

for card in cards.keys():
    score2 += cards[card]['quantity']
    for i in range(1, cards[card]['match']+1):
        if card+i in cards:
            cards[card+i]['quantity'] += cards[card]['quantity']

print("Partie 2 :", score2)