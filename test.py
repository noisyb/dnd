import unittest, random
import dice, chara, randchara

class dice_rolls(unittest.TestCase):

	def test_rolling(self):
		test_dice = dice.dice_group(sides=20,num=100,type_of='test')
		print('\n---D20 ROLLS---')
		print(sorted(test_dice.result))

class character_generics(unittest.TestCase):
	
	def test_char_abilities(self):
		char0 = chara.character()
		with self.assertRaises(KeyError):
			char0.abi_get('str')
		with self.assertRaises(Exception):
			char0.abi_set(plarp=17)
		char0.abi_set(str=9)
		with self.assertRaises(KeyError):
			char1 = chara.character()
			char1.abi_get('str')
		self.assertEqual(char0.abi_mod('str'),-1)
	
	def test_char_xp(self):
		char0 = chara.character()
		char0.xp = 0
		self.assertEqual(char0.lvl,1)
		char0.xp = 999999999
		self.assertEqual(char0.lvl,20)
		for x in range(0,20):
			char0.lvl = x+1
			self.assertEqual(char0.lvl,x+1)

	def test_char_skills(self):
		char0 = chara.character()
		char0.abi_set(str=9,dex=20,con=10,int=1,wis=10,cha=10)
		char0.skills = ['acro','arca','inti']
		char0.lvl = 4
		self.assertEqual(char0.ski_mod('acro'),7)
		self.assertEqual(char0.ski_mod('athl'),-1)
		self.assertEqual(char0.ski_mod('arca'),-3)
		self.assertEqual(char0.ski_mod('inti'),2)
		char1 = chara.character()
		with self.assertRaises(IndexError):
			a = char1.skills[0]
		char0.lvl = 5
		self.assertEqual(char0.ski_mod('arca'),-2)
	
	def test_char_hp(self):
		char0 = chara.character()
		char0.max_hp = 10
		char0.damage(10, None)
		self.assertEqual(char0.missing_hp,-10)
		self.assertTrue('incapacitated' in char0.status_effects)
		self.assertTrue('unconscious' in char0.status_effects)
		char0.heal(20)
		self.assertEqual(char0.missing_hp,0)
		self.assertFalse('incapacitated' in char0.status_effects)
		self.assertFalse('unconscious' in char0.status_effects)
		char0.set_temphp(12)
		self.assertEqual(char0.hp,22)
		char0.set_temphp(11)
		self.assertEqual(char0.hp,21)

class random_characters(unittest.TestCase):

	def test_rand_char(self):
		random_fighter = randchara.full_rand_char('figh')
		random_fighter.p_print()

class input_characters(unittest.TestCase):

	def test_grex(self):
		grex = chara.character()
		grex.name = 'Grex Arkon'
		grex.race_abrv = 'sildrag'
		grex.alignment = 'NG'
		grex.abi_set(str=20,dex=14,con=15,int=14,wis=11,cha=16)	
		grex.class_abrv = 'figh'
		grex.xp = 4584
		grex.skills = ['athl','inti','perf','surv']
		grex.max_hp = 35

		self.assertEqual(grex.abi_mod('str'),5)
		self.assertEqual(grex.abi_mod('dex'),2)
		self.assertEqual(grex.abi_mod('con'),2)
		self.assertEqual(grex.abi_mod('int'),2)
		self.assertEqual(grex.abi_mod('wis'),0)
		self.assertEqual(grex.abi_mod('cha'),3)
		self.assertEqual(grex.lvl,4)
		self.assertEqual(grex.prof,2)
		self.assertEqual(grex.ski_mod('acro'),2)
		self.assertEqual(grex.ski_mod('anim'),0)
		self.assertEqual(grex.ski_mod('arca'),2)
		self.assertEqual(grex.ski_mod('athl'),7)
		
		grex.p_print()
		
if __name__=='__main__':
	unittest.main()
