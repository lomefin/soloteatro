from lib.imports import *

class AddSeason(llhandler.LLHandler):
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

class AddSeasonToMontage(llhandler.LLHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def get(self,montage_slug):

		self.auth_check()
		self.internal_get(montage_slug)

	def internal_get(self,montage_slug):

		montage = self.get_or_404(STMontage.all().filter('slug =',montage_slug).get())
		logging.debug('Looking for ' + montage_slug + "... " + str(montage))
		self.set('montage',montage)

		self.render('add_season')

	def internal_post(self):

		# start = db.DateTimeProperty()
		# end = db.DateTimeProperty()
		# prices = db.StringListProperty()
		# venue = db.ReferenceProperty(STVenue,collection_name='seasons')
		# montage = db.ReferenceProperty(STMontage,collection_name='seasons')
		

		# repetition = db.IntegerProperty()

		# #Technical Sheet
		# cast = db.StringListProperty()
		# producer = db.StringProperty()
		# technical_team = db.StringListProperty()
		season = STSeason()

class AddSeasonExpress(llhandler.LLHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		venue_list = STVenue.all()
		self.render('add_season_express',template_values={'venue_list':venue_list})

	def internal_post(self):
		
		montage = STMontage()
		montage.name = self.param('montage_name')
		montage.director = self.param('montage_director')
		montage.genre = self.param('montage_genre')
		montage.description = self.param('montage_description')
		montage.slug = Slugger.slugify(str(montage.name) + " de "+str(montage.director))

		montage.put()
		self.param_dump()
		season = STSeason()
		season.montage = montage.key()
		season.venue = db.Key(encoded = self.param("season_venue"))
		season.start = datetime.datetime.strptime(self.param("season_start"),"%m/%d/%Y")
		season.end = datetime.datetime.strptime(self.param("season_end"),"%m/%d/%Y")

		season.put()


