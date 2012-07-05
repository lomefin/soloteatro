from lib.imports import *

class ShowReports(llhandler.LLGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	

	def internal_get(self):

		self.render('dashboard')
		
