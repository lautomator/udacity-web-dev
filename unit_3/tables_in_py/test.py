# Ordering a list based on an 'ID' parameter.

inventory = [
    (12, 'apple'),
    (1, 'pear'),
    (18, 'banana'),
    (4, 'prune'),
    (3, 'peach'),
    (0, 'fig'),
]

inventory.sort()

print inventory
# [(0, 'fig'), (1, 'pear'), (3, 'peach'), (4, 'prune'), (12, 'apple'), (18, 'banana')]

for item in inventory:
    print item[1]
# fig
# pear
# peach
# prune
# apple
# banana
