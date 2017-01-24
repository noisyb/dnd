import dice, random
import chara

#order of abilities aka abi is important, as highest score is set
#to first ability and so on down
ARCHETYPE_OPTS = dict( \
	figh=dict(abi=['str','con','dex','wis','cha','int'], \
	roll_level='std',cla='figh',races=['human','horc','elf'], \
	skills=['athl','perc','insi','surv'],skills_no=4, \
	lvl=5,align='CE') \
	)

def full_rand_char(archetype,opt_dict=None):
	if opt_dict==None:
		options = ARCHETYPE_OPTS[archetype]
	else:
		options = opt_dict[archetype] #write logic here to take input for randomisations
		pass

	the_char = chara.character()
	the_char.name = 'Random Character' #FIXME - make a random name generator python
	the_char.class_abrv = options['cla']
	the_char.race_abrv = random.choice(options['races'])
	the_char.lvl = options['lvl']
	the_char.alignment = options['align']
	
	rolls = []
	
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
	
	#sampling means a set of options can be selected from with no repeats
	#FIXME - probably a good idea to implement this in more scenarioes
	the_char.skills = random.sample(options['skills'],options['skills_no'])
	
	return the_char
