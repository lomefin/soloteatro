
from lib.imports import *

class DefaultHandler(llhandler.LLHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		logging.info(os.path.dirname(__file__))
		self.render('index',template_values={})

def main():
  LLApp([('/', DefaultHandler)])
