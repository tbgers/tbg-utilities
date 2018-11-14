with open('rbs.txt') as f:
    rainbows = f.read().splitlines()

print(rainbows[6::7])
