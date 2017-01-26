import configparser

class rules:

	def __init__(self):
		ez_config = configparser.ConfigParser()
		ez_config.read('./config/5e.ini')
		race_config = configparser.ConfigParser()
		race_config.read('./config/5e_races.ini')
		self.ability_score = ability_score()
		self.class_features = class_features(ez_config)
		self.skills = skills(ez_config)
		self.level = level()
		self.alignment = alignment(ez_config)
		self.status_effects = status_effects()
		self.race = race(race_config)

class ability_score:
	def __init__(self):
		self.names = ['str','dex','con','int','wis','cha']
		self.name_err = Exception('Ability not in recognized list')
		self.val_err = Exception('Ability integer too low or high')
		
class class_features:
	def __init__(self,config):
		self.names = config['class_names']
		self.abrv = []
		for key, val in self.names.items():
			self.abrv.append(key)

class skills:
	def __init__(self,config):
		self.ability = config['skill_abi']
		self.abrv = []
		for key, val in self.ability.items():
			self.abrv.append(key)
		self.names = config['skill_names']

class level:
	def __init__(self):
		self.xp_per = [300,900,2700,6500,14000,23000,34000,48000,64000,85000,100000,120000,140000,165000,195000,225000,265000,305000,355000]

class alignment:
	def __init__(self,config):
		self.abrv = []
		self.names = config['alignment_names']
		for key, val in self.names.items():
			self.abrv.append(key)

class status_effects:
	def __init__(self):
		self.names = ['blind','charmed','deaf','exhausted','frightened','incapacitated','invisible','paralyzed','petrified','poisoned','prone','restrained','stunned','unconscious']

class race:
	def __init__(self,config):
		#use the .sections() for more shit - maybe status_effects?
		self.abrv = config.sections()
		self.names = dict()
		for x in self.abrv:
			self.names[x] = config[x]['name']

a = rules()
print('ok')
