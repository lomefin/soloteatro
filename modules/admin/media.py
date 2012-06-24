from lib.imports import *

class AddMediaToSeason(llhandler.LLGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def get(self, *args):

		for arg in args:
			logging.debug("ARG:\t" + str(arg))
		self.auth_check()
		self.internal_get(montage_slug,season_numeral)

	def internal_get(montage_slug,season_numeral):

		montage = self.get_or_404(STMontage.all().filter('slug =',montage_slug).get())

		self.render('add_montage',template_values={})

	def internal_post(self):
		montage = STMontage()
		montage.name = self.param('montage_name')
		montage.director = self.param('montage_director')
		montage.genre = self.param('montage_genre')
		montage.description = self.param('montage_description')
		montage.slug = Slugger.slugify(str(montage.name) + " de "+str(montage.director))

		montage.put()