from lib.imports import *

class AddPlay(llhandler.LLHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		self.render('add_play',template_values={})