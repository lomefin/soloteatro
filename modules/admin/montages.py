from lib.imports import *

class AddMontage(llhandler.LLHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		self.render('add_montage',template_values={})

	def internal_post(self):
		montage = STMontage()
		montage.name = self.param('montage_name')
		montage.director = self.param('montage_director')
		montage.genre = self.param('montage_genre')
		montage.description = self.param('montage_description')
		montage.slug = Slugger.slugify(str(montage.name) + " de "+str(montage.director))

		montage.put()

class ViewMontage(llhandler.LLHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def transitional_get(self, args):

		self.internal_get(args[0])
		

	def internal_get(self,slug):
		logging.debug("Looking montage with slug ["+slug+"]")
		montage = self.retrieve_or_404(STMontage.all().filter('slug =',slug).get())
		logging.debug(montage)
		self.render('view_montage',template_values={'montage':montage})	

class ListMontages(llhandler.LLHandler):

	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		montage_list = STMontage.all()
		self.render('list_montages',template_values={'montage_list':montage_list})

	def internal_post(self):
		montage = STMontage()
		montage.name = self.param('montage_name')
		montage.director = self.param('montage_director')
		montage.description = self.param('montage_description')
		montage.slug = Slugger.slugify(str(montage.name) + " de "+str(montage.director))

		montage.put()