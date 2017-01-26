import math, configparser
import dice, data_5e

ruleset = data_5e.rules()

#Effectively, lots of abilities have common damage, mods, range attributes, 
#might be worth making a config file parser for it

class character:

	def __init__(self):
		self.abi = dict() 
		self.name = ''
		self._xp = 0
		#background
		self.bkg = ''
		#who plays it (can be dm)
		self.player = ''
		self._class = ''
		self._race = ''
		self.alignment = ''
		self.skills = []
		self.items = dict()
		self.feats = []
		#FIXME - probs need to alter this structure self.spells = []
		#health variables
		self._hp = 0
		self._maxhp = 0
		self._temphp = 0
		#status effects
		self._status = dict()

	#Pretty Print character or single section	
	def p_print(self,section='full'):
		
		print ('\nCharacter: ' + self.name)
		print ('Race: ' + self.race_name)
		print ('Level/Class: ' + str(self.lvl) + ' ' + self.class_name)
		print ('Max Hp: ' + str(self.max_hp))
		print ('Alignment: ' + self.alignment_name)
		if section in ['full','abi']:
			print('---ABILITY SCORES---')
			for x in ruleset.ability_score.names:
				print(x + ': ' + str(self.abi_get(x)) + ' : ' + str(self.abi_mod(x)))

		if section in ['full','ski']:
			print('----SKILL MODIFIERS----')
			for x in ruleset.skills.abrv:
				skill_string = '{:<17} {:>3}'.format(ruleset.skills.names[x] + ': ', str(self.ski_mod(x)))
				if x in self.skills: skill_string += ' X'
				print(skill_string)
	
	#Status-related functions
	def set_status(self,status_effect,reason):
		if status_effect not in ruleset.status_effects.names: raise KeyError
		if status_effect in self._status: 
			self._status[status_effect].append(reason)
		else:
			self._status[status_effect] = [reason]

	def rm_status(self,reason):
		removed_statuses = []
		for key, val in self._status.items():
			val.remove(reason)
			#if no more reasons for a particular
			#status are left remove it
			if not val: removed_statuses.append(key)
		for key in removed_statuses:
			del self._status[key]
		
	@property
	def status_effects(self):
		status_list = []
		for key, val in self._status.items():
			status_list.append(key)
		return status_list

	#Health management functions
	@property
	def hp(self):
		return self._hp + self._temphp

	@property
	def max_hp(self):
		return self._maxhp

	@max_hp.setter
	def max_hp(self,maxhp):
		self._maxhp = maxhp

	@property
	def missing_hp(self):
		return self._hp - self._maxhp

	def damage(self,amount,type_of):
		
		if type_of in ['list of player abilities which reduce damage']:
			#FIXME - do the appropriate reduction/increase
			amount /= 2
			amount *= 2
		
		self._temphp -= amount

		if self._temphp <= 0:
			self._hp += self._temphp
			self._temphp = 0

		if self._hp <= 0:
			self._hp = 0
			self.set_status('unconscious','hp0')
			self.set_status('incapacitated','hp0')
	
	def heal(self,amount):
		if amount <= 0: raise Exception('Tried to heal nothing/negative')
		self._hp += amount
		if self._hp > self._maxhp: self._hp = self._maxhp
		self.rm_status('hp0')

	def set_temphp(self,amount):
		self._temphp = amount
	
	#Alignment pretty name
	@property
	def alignment_name(self):
		return ruleset.alignment.names[self.alignment]
	
	#Race related functions
	@property
	def race_abrv(self):
		return self._race

	@race_abrv.setter
	def race_abrv(self,abrv):
		#FIXME - set the race abilities and other features here
		self._race = abrv

	@property
	def race_name(self):
		name = ruleset.race.names[self.race_abrv]
		return name

	#Class related functions
	@property
	def class_abrv(self):
		return self._class

	@class_abrv.setter
	def class_abrv(self,abrv_name):
		self._class = abrv_name

	@property
	def class_name(self):
		return ruleset.class_features.names[self.class_abrv]

	#Ability related functions
	def abi_set(self,**kwargs):
		for key, val in kwargs.items():
			if val < 0 or val > 40:
				raise ruleset.ability_score.val_err
			if key not in ruleset.ability_score.names:
				raise ruleset.ability_score.name_err
			self.abi[key] = val

	def abi_get(self,ability):
		if ability not in ruleset.ability_score.names:
			raise ruleset.ability_score.name_err
		return self.abi[ability]

	#Modifier derived from ability score
	def abi_mod(self,ability):
		if ability not in ruleset.ability_score.names:
			raise ruleset.ability_score.name_err
		score = self.abi[ability]
		if score < 10: score -= 1
		return math.trunc((score-10)/2)

	#XP and Level related functions
	@property
	def xp(self):
		return self._xp
	
	@xp.setter
	def xp(self, value):
		self._xp = value

	#Returns level as integer
	@property
	def lvl(self):
		xp = self._xp
		lvl = 1
		for x in ruleset.level.xp_per:
			xp = xp - x
			if xp < 0:
				return lvl
			lvl += 1
		return 20
	
	#Convert level number to minimum possible XP
	#and set the XP to that number
	@lvl.setter
	def lvl(self,value):
		self._xp = 0
		xp = 0
		for x in range(0,value):
			y = x-1
			if y >= 0:
				lvl_xp = ruleset.level.xp_per[y]
				xp += lvl_xp
		self._xp = xp

	#FIXME - Levels the character up - rather than just setting their xp etc.
	#This is the stuff where we get to setting abilities per class, rolling hp
	#First level levelling could potentially include a more detailed character prompt
	def gain_xp(self):
		pass

	def gain_levels(self):
		pass
		
	#Proficiency score derived from level
	@property
	def prof(self):
		level = self.lvl
		return int(2+((level-1)/4))
	
	#Skill modifier per skill
	def ski_mod(self,skill):
		skill_mod = 0
		if skill in self.skills: skill_mod += self.prof
		skill_mod += self.abi_mod(ruleset.skills.ability[skill])
		return skill_mod
