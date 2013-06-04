from lib.imports import *

class NewMontage(llhandler.LLGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		self.set('montages',STMontage.all())
		self.render('/admin/new_montage')


class AddMontage(llhandler.LLGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		#open_montages_names = db.GqlQuery("SELECT STMontage.name FROM STMontage WHERE status = :1",'Open')
		open_montages = STMontage.all().filter('status =','Open').get()
		self.set('open_montages',open_montages)
		self.render('/admin/add_montage',template_values={})

	def internal_post(self):
		montage = STMontage()
		montage.name = self.param('montage_name')
		montage.director = self.param('montage_director')
		montage.genre = self.param('montage_genre')
		montage.description = self.param('montage_description')
		montage.slug = Slugger.slugify(montage.name + " de "+montage.director)

		montage.put()

class ViewMontage(llhandler.LLGAEHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def transitional_get(self, args):

		self.internal_get(args[0])
		

	def internal_get(self,slug):
		logging.debug("Looking montage with slug ["+slug+"]")
		montage = self.retrieve_or_404(STMontage.all().filter('slug =',slug).get())
		self.render('/admin/view_montage',template_values={'montage':montage})	

class ListMontages(llhandler.LLGAEHandler):

	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		montage_list = STMontage.all()
		self.render('/admin/list_montages',template_values={'montage_list':montage_list})
