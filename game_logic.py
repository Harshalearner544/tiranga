import random

ODDS = {
    'Red': 2,
    'Green': 2,
    'Violet': 4.5
}

def generate_result(bets):
    """
    bets: list of color choices in the current round
    Result color = least selected color
    """
    counts = {'Red': 0, 'Green': 0, 'Violet': 0}

    for b in bets:
        if b in counts:
            counts[b] += 1

    # choose least selected color
    min_count = min(counts.values())
    least_colors = [c for c, v in counts.items() if v == min_count]
    color = random.choice(least_colors)

    # generate number matching color
    if color == 'Green':
        number = random.choice([1, 3, 7, 9])
    elif color == 'Red':
        number = random.choice([2, 4, 6, 8])
    else:
        number = 0

    return number, color