with open('input/input2.txt', 'r') as f:
    data = f.read().splitlines()

def is_forbidden(draw):
    if 'red' not in draw.keys():
        draw['red'] = 0
    if 'green' not in draw.keys():
        draw['green'] = 0
    if 'blue' not in draw.keys():
        draw['blue'] = 0
    if draw['red'] > 12 or draw['green'] > 13 or draw['blue'] > 14:
        return True
    return False

games = {}
for row in data:
    row_data = row.split(":")
    game = int(row_data[0].replace("Game ", ""))
    draws = row_data[1].split(";")
    game_array = []
    for draw in draws:
        colors = draw.split(',')
        draw_dict = {}
        for color in colors:
            color = color.strip().split(" ")
            draw_dict[color[1]] = int(color[0])
        game_array.append(draw_dict)
    games[game] = game_array

count1 = 0
for g in games.keys():
    if not any([is_forbidden(d) for d in games[g]]):
        count1 += g

print(count1)

count2 = 0
for g in games.keys():
    min_red = 0
    min_green = 0
    min_blue = 0
    for draw in games[g]:
        min_red = max(min_red, draw['red'])
        min_green = max(min_green, draw['green'])
        min_blue = max(min_blue, draw['blue'])

    count2 += min_red*min_green*min_blue

print(count2)