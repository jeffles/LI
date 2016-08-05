import itertools
x = [1, 2, 3, 4, 5, 6]
r = [p for p in itertools.product(x, repeat=4)]

odds = {}
total = 0

for d in r:
    score = sum(d)-min(d)
    # print(score, d)
    odds[score] = odds.get(score, 0) + 1
    total += 1

for odd in odds:
    print(odd, odds[odd], odds[odd]/ total * 100)
print(odds)

