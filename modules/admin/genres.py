from lib.imports import *

class AdminGenres(llhandler.LLGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		self.set('genre_list', STGenre.all().order('-rating'))
		self.render('admin_genre')

	def internal_post(self):
		genre = STGenre()
		genre.name = self.param("genre_name")
		genre.slug = Slugger.slugify(genre.name)
		genre.rating = int(self.param("genre_rating"))
		new_genre = genre.put()
		if not new_genre:
			self.set_flash('Hubo un problema agregando el género.')
		else:
			self.set_flash("Género agregado")
		self.internal_get()



