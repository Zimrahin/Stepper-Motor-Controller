import json

class config(object):
	def __init__(self):
		super(config, self).__init__()
		self.dict = {}
		self.readJSON()

	def writeJSON(self):
		with open('config.json', "w", encoding='utf-8') as write:
			json.dump(self.dict, write, indent=4)

	def readJSON(self):
		with open('config.json', "r", encoding='utf-8') as reader:
			settings = json.loads(reader.read())
			self.dict = settings

if __name__ == '__main__':
	config_class = config()
	print(config_class.dict)