import dice, math

ABILITY_SCORE_NAMES = ['str','dex','con','int','wis','cha']
ABILITY_NAME_ERR = Exception('Ability not in recognized list')
CHAR_CLASSES = ['barb','bard','cler','drui','figh','monk','pala','rang','rogu','sorc','warl','wiza']
SKILL_DICT = dict(acro='dex',anim='wis',arca='int',athl='str',dece='cha',hist='int',insi='wis',inti='cha',inve='int',medi='wis',natu='int',perc='wis',perf='cha',pers='cha',reli='int',slei='dex',stea='dex',surv='wis')
SKILL_NAMES = []
for key in SKILL_DICT.items():
	SKILL_NAMES.append(key)
LVL_CHART = [300,900,2700,6500,14000,23000,34000,48000,64000,85000,100000,120000,140000,165000,195000,225000,265000,305000,355000]

class ability_scores:

	def __init__(self):
		self._scores = dict()

class character:

	def __init__(self,**kwargs):
		self.abi = dict() 
		self.name = ''
		self._xp = 0
		#background
		self.bkg = ''
		#who plays it (can be dm)
		self.player = ''
		self.class_ = ''
		self.race = ''
		self.alignment = ''
		self.char_desc = ''
		self.skills = []
		self.items = dict()
		self.feats = []
		self.spells = []

	def abi_set(self,**kwargs):
		for key, val in kwargs.items():
			if val < 0 or val > 40:
				raise ABILITY_NAME_ERR #FIXME
			if key not in ABILITY_SCORE_NAMES:
				raise ABILITY_NAME_ERR 
			self.abi[key] = val

	def abi_get(self,ability):
		if ability not in ABILITY_SCORE_NAMES:
			raise ABILITY_NAME_ERR
		return self.abi[ability]

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
		

	@property
	def prof(self):
		level = self.lvl
		return int(2+((level-1)/4))

	def ski_mod(self,skill):
		skill_mod = 0
		if skill in self.skills: skill_mod += self.prof
		skill_mod += self.abi_mod(SKILL_DICT[skill])
		return skill_mod
