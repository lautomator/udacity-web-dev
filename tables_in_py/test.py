# Ordering a list based on an 'ID' parameter.

results = [
	(12, 'apple'),
	(1, 'pear'),
	(18, 'banana'),
	(4, 'prune'),
	(3, 'peach'),
	(0, 'fig'),
]

results.sort()

print results
# [(0, 'fig'), (1, 'pear'), (3, 'peach'), (4, 'prune'), (12, 'apple'), (18, 'banana')]

for item in results:
	print item[1]
# fig
# pear
# peach
# prune
# apple
# banana
