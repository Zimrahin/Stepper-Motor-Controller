__author__ = 'github.com/Zimrahin'
# Classes to handle JSON writing and reading. This is used for saving/reading routine settings and reading a colour palette.

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

class JSONwriter(object):
	def __init__(self, file):
		super(JSONwriter, self).__init__()
		self.dict = {}
		self.file = file

	def writeJSON(self):
		with open(self.file, "w", encoding='utf-8') as write:
			json.dump(self.dict, write, indent=4)


if __name__ == '__main__':
	config_class = JSONreader('config.json')
	print(config_class.dict)