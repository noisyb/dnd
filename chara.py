import math, configparser
import dice

ez_config = configparser.ConfigParser()
ez_config.read('./config/5e.ini')

#Ability score constants
ABILITY_SCORE_NAMES = ['str','dex','con','int','wis','cha']
ABILITY_NAME_ERR = Exception('Ability not in recognized list')
ABILITY_VAL_ERR = Exception('Ability int too low or high')

#Class constants
CLASS_DICT = ez_config['class_names']
CLASS_ABRV = []
for key, val in CLASS_DICT.items():
	CLASS_ABRV.append(key)

#Skill constants
SKILL_ABI = ez_config['skill_abi']
SKILL_ABRV = []
for key, val in SKILL_ABI.items():
	SKILL_ABRV.append(key)
SKILL_NAMES = ez_config['skill_names']

#Level constants
LVL_CHART = [300,900,2700,6500,14000,23000,34000,48000,64000,85000,100000,120000,140000,165000,195000,225000,265000,305000,355000]

ALIGNMENTS = ['LG','NG','CG','LN','NN','CN','LE','NE','CE']

#Race information/modifiers/extra abilities

race_config = configparser.ConfigParser()
race_config.read('./config/5e_races.ini')

RACE_ABRV = race_config.sections()
RACE_NAMES = dict()
for x in RACE_ABRV:
	RACE_NAMES[x] = race_config[x]['name']


#Effectively, lots of abilities have common damage, mods, range attributes, 
#might be worth making a config file parser for it

class character:

	def __init__(self,**kwargs):
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
		self.char_desc = ''
		self.skills = []
		self.items = dict()
		self.feats = []
		self.spells = []

	#Pretty Print character or single section	
	def p_print(self,section='full'):
		
		print ('\nCharacter: ' + self.name)
		print ('Race: ' + self.race_name)
		print ('Level/Class: ' + str(self.lvl) + ' ' + self.class_name)
		if section in ['full','abi']:
			print('---ABILITY SCORES---')
			for x in ABILITY_SCORE_NAMES:
				print(x + ': ' + str(self.abi_get(x)) + ' : ' + str(self.abi_mod(x)))

		if section in ['full','ski']:
			print('----SKILL MODIFIERS----')
			for x in SKILL_ABRV:
				skill_string = '{:<17} {:>3}'.format(SKILL_NAMES[x] + ': ', str(self.ski_mod(x)))
				if x in self.skills: skill_string += ' X'
				print(skill_string)
	
	@property
	def race_abrv(self):
		return self._race

	@race_abrv.setter
	def race_abrv(self,abrv):
		self._race = abrv

	@property
	def race_name(self):
		name = RACE_NAMES[self._race]
		return name

	@property
	def class_abrv(self):
		return self._class

	@class_abrv.setter
	def class_abrv(self,abrv_name):
		self._class = abrv_name

	@property
	def class_name(self):
		return CLASS_DICT[self._class]

	def abi_set(self,**kwargs):
		for key, val in kwargs.items():
			if val < 0 or val > 40:
				raise ABILITY_VAL_ERR
			if key not in ABILITY_SCORE_NAMES:
				raise ABILITY_NAME_ERR 
			self.abi[key] = val

	def abi_get(self,ability):
		if ability not in ABILITY_SCORE_NAMES:
			raise ABILITY_NAME_ERR
		return self.abi[ability]

	#Modifier derived from ability score
	def abi_mod(self,ability):
		if ability not in ABILITY_SCORE_NAMES:
			raise ABILITY_CALL_ERR
		score = self.abi[ability]
		if score < 10: score -= 1
		return math.trunc((score-10)/2)

	@property
	def xp(self):
		return self._xp
	
	@xp.setter
	def xp(self, value):
		self._xp = value

	#Returns level as int
	@property
	def lvl(self):
		xp = self._xp
		lvl = 1
		for x in LVL_CHART:
			xp = xp - x
			if xp < 0:
				return lvl
			lvl += 1
		return 20
	
	#Convert level number to minimum possible XP
	@lvl.setter
	def lvl(self,value):
		self._xp = 0
		xp = 0
		for x in range(0,value):
			y = x-1
			if y >= 0:
				lvl_xp = LVL_CHART[y]
				xp += lvl_xp
		self._xp = xp
		
	#Proficiency score derived from level
	@property
	def prof(self):
		level = self.lvl
		return int(2+((level-1)/4))
	
	#Skill modifier per skill
	def ski_mod(self,skill):
		skill_mod = 0
		if skill in self.skills: skill_mod += self.prof
		skill_mod += self.abi_mod(SKILL_ABI[skill])
		return skill_mod
