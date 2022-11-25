__author__ = 'github.com/Zimrahin'

import json

class JSONreader(object):
	def __init__(self, file):
		super(JSONreader, self).__init__()
		self.dict = {}
		self.file = file
		self.readJSON()

	def writeJSON(self):
		with open(self.file, "w", encoding='utf-8') as write:
			json.dump(self.dict, write, indent=4)

	def readJSON(self):
		with open(self.file, "r", encoding='utf-8') as reader:
			settings = json.loads(reader.read())
			self.dict = settings

if __name__ == '__main__':
	config_class = JSONreader()
	print(config_class.dict)