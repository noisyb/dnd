#dice shit

import random

class dice_group:
	
	def __init__(self,sides,num=1,type_of=None):
		self.sides = sides
		self.num = num
		self.type_of = type_of
		self.result = roll(self)

	def reroll(self):
		self.result = roll(self)
	
	def total(self):
		total = 0
		for x in self.result:
			total += x
		return total

def roll(dice_grp):
	dice_list = []
	for x in range(0,dice_grp.num):
		dice_list.append(random.randint(1,dice_grp.sides))
	return dice_list

