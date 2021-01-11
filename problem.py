
class RelaxedProblem(): 
	def __init__(self, active, passive, alphabet):
		self.active = active
		self.passive = passive
		self.alphabet = alphabet

	def getActive(self):
		return self.active

	def getPassive(self):
		return self.passive

	def getAlphabet(self):
		return self.alphabet

class CanonicalProblem():
	def __init__(self, active, passive, alphabet):
		self.active = active
		self.passive = passive
		self.alphabet = alphabet

	def getActive(self):
		return str(self.active)

	def getPassive(self):
		return self.passive

	def getAlphabet(self):
		return self.alphabet

	"""def getDegree(self): 
		res = self.active.split('\n')
		return len(res[0].split(' '))"""
