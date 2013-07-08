from lib.imports import *

class AddMontage(llhandler.LLGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		#open_montages_names = db.GqlQuery("SELECT STMontage.name FROM STMontage WHERE status = :1",'Open')
		#open_montages = STMontage.all().filter('status =','Open').get()
		#self.set('open_montages',open_montages)
		self.set('genres',STGenre.all().order('rating'))
		self.render('/admin/add_montage',template_values={})

	def internal_post(self):
		montage = STMontage()
		montage.name = self.param('montage_name')
		montage.director = self.param('montage_director')
		montage.writer	= self.param("montage_writer")
		montage.company = self.param('montage_company')
		montage.genre = STGenre.all().filter('slug =',self.param('montage_genre')).get()
		montage.description = self.param('montage_description')
		montage.slug = Slugger.slugify(montage.name + " de "+montage.director)
		montage.external_gallery = self.param('montage_gallery')
		montage_result = montage.put()
		if montage_result:
			self.set_flash('Montaje creado')
			self.redirect_to('/admin/montages/'+montage.slug+'/edit')
		else:
			self.set_flash('Error creando montaje')
			self.redirect_to('/admin/montages/new')

class EditMontage(llhandler.LLGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)

	def transitional_get(self, args):
		self.internal_get(args[0])

	def transitional_post(self, args):
		self.internal_post(args[0])

	def internal_get(self, slug):
		montage = self.retrieve_or_404(STMontage.all().filter('slug =',slug).get())
		self.set('genres',STGenre.all().order('rating'))
		self.set('montage', montage)
		self.render('/admin/add_montage')

	def internal_post(self,slug):
		montage = self.retrieve_or_404(STMontage.all().filter('slug =',slug).get())
		montage.name = self.param('montage_name')
		montage.director = self.param('montage_director')
		montage.writer	= self.param("montage_writer")
		montage.company = self.param('montage_company')
		montage.genre = STGenre.all().filter('slug =',self.param('montage_genre')).get()
		montage.description = self.param('montage_description')
		montage.slug = Slugger.slugify(montage.name + " de "+montage.director)
		montage.external_gallery = self.param('montage_gallery')
		montage_result = montage.put()
		if montage_result:
			self.set_flash('Montaje editado')
			self.redirect_to('/admin/montages/'+montage.slug+'/edit')
			#self.render('/admin/view_montage',template_values={'montage':montage})
		else:
			self.set_flash('Error editando montaje')
			self.redirect_to('/admin/montages/'+slug+'/edit')


class ViewMontage(llhandler.LLGAEHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def transitional_get(self, args):

		self.internal_get(args[0])
		

	def internal_get(self,slug):
		montage = self.retrieve_or_404(STMontage.all().filter('slug =',slug).get())
		self.render('/admin/view_montage',template_values={'montage':montage})	

class ListMontages(llhandler.LLGAEHandler):

	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		montage_list = STMontage.all()
		self.render('/admin/list_montages',template_values={'montage_list':montage_list})
