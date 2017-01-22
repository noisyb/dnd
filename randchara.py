import dice, chara

ARCHETYPE_OPTS = dict( \
	figh=dict(abi=['str','con','dex','wis','cha','int'], \
	roll_level='std',cla='figh', \
	skills=['athl','perc','insi','surv']) \
	)

def full_rand_char(archetype):
	options = ARCHETYPE_OPTS[archetype]
	rolls = []
	
	the_char = chara.character()

	the_char.class_abrv = options['cla']

	for x in range(0,6):
		y = dice.dice_group(6,4)
		if options['roll_level'] == 'hero':
			y.result.sort()
		y.result = y.result[-3:]
		rolls.append(y.total())

	rolls.sort(reverse=True)
	for ability in options['abi']:
		the_char.abi[ability] = rolls[0]
		rolls = rolls[1:]

	the_char.skills = options['skills']
	
	return the_char
