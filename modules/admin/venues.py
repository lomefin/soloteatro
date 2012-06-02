from lib.imports import *

class AddVenue(llhandler.LLHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		self.render('add_venue',template_values={})

class ViewVenue(llhandler.LLHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def get(self,venue_code):
		self.internal_get(venue_code)

	def internal_get(self,venue_code):
		self.render('view_venue',template_values={})