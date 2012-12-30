from lib.imports import *

class AddPlay(llhandler.LLGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		venue_list = STVenue.all()
		self.render('/admin/add_play',template_values={'venue_list':venue_list})

	def internal_post(self):
		pass


