import configparser

		#FIXME - Refactor below dict creations as functions at some point!!!
		#They can just access config directly, rather than via new dicts
		#This will require a lil work in chara.py
		#This model also works better than the dict-building in other classes here

#self.abrv is standard - and a list of all possible options in the class
#this could in future allow generic errors generated per class - Exception('Option not in ' + x + ' list')
#also this allows something to iterate thru functions - abrv should be the transferred ID between objs and functs
#or might just change this to 'names' as the default and remove abrv entirely

class rules:

	def __init__(self):
		ez_config = configparser.ConfigParser()
		ez_config.read('./config/5e.ini')
		skill_config = configparser.ConfigParser()
		skill_config.read('./config/5e_skills.ini')
		race_config = configparser.ConfigParser()
		race_config.read('./config/5e_races.ini')
		self.ability_score = ability_score()
		self.class_features = class_features(ez_config)
		self.skills = skills(skill_config)
		self.level = level()
		self.alignment = alignment(ez_config)
		self.status_effects = status_effects()
		self.race = race(race_config)

class ability_score:
	def __init__(self):
		#FIXME - change to config file with at least names
		self.abrv = ['str','dex','con','int','wis','cha']
		self.name_err = Exception('Ability not in recognized list')
		self.val_err = Exception('Ability integer too low or high')
		
class class_features:
	def __init__(self,config):
		self.names = config['class_names']
		self.abrv = []
		#FIXME - hold off on refactoring this as a funct until
		#There's a better class config file
		for key, val in self.names.items():
			self.abrv.append(key)

class skills:
	def __init__(self,config):
		self._config = config
		self.abrv = config.sections()

	def name(self,abrv):
		return self._config[abrv]['name']

	def ability(self,abrv):
		return self._config[abrv]['abi']

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
