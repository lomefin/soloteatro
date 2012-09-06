from lib.imports import *

class AddSeason(llhandler.LLGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		self.render('add_montage',template_values={})

	def internal_post(self):
		montage = STMontage()
		montage.name = self.param('montage_name')
		montage.director = self.param('montage_director')
		montage.genre = db.Category(self.param('montage_genre'))
		montage.description = self.param('montage_description')
		montage.slug = Slugger.slugify(str(montage.name) + " de "+str(montage.director))

		montage.put()

class AddSeasonToMontage(llhandler.LLGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def transitional_get(self,args):

		self.auth_check()
		self.internal_get(args[0])

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

class AddSeasonExpress(llhandler.LLGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		venue_list = STVenue.all()
		self.render('add_season_express',template_values={'venue_list':venue_list})

	def daterange(self,start_date, end_date):

		for n in range((end_date - start_date).days):
			yield start_date + timedelta(n)

	def internal_post(self):
		
		#The Montage
		montage = STMontage()
		montage.name = self.param('montage_name')
		montage.director = self.param('montage_director')
		montage.writer	= self.param("montage_writer")
		montage.genre = db.Category(self.param('montage_genre'))
		montage.description = self.param('montage_description')
		montage.slug = Slugger.slugify(montage.name + " de "+montage.director)
		montage.put()
		
		seasons_for_this_montage = montage.seasons.count()
		
		#The first season
		season = STSeason()
		season.montage = montage.key()
		season.venue = db.Key(encoded = self.param("season_venue"))
		season.start = datetime.datetime.strptime(self.param("season_start"),"%m/%d/%Y")
		season.end = datetime.datetime.strptime(self.param("season_end"),"%m/%d/%Y")
		season.repetition = seasons_for_this_montage + 1
		season.status = db.Category("Open")
		season.cast = self.param("season_cast").split(",")
		season.genre = montage.genre
		season.put()

		#Le Plays for that season
		showtimes = []
		for (idx,day) in enumerate(['monday','tuesday','wednesday','thursday','friday','saturday','sunday']):
			showtimes.insert(idx,None)
			if self.param('plays_on_'+day):
				showtimes[idx] = datetime.datetime.strptime(self.param(day + '_showtime'),"%H:%M").time()

		logging.debug(showtimes)
		
		for single_date in self.daterange(season.start, season.end):
			showtime = showtimes[single_date.weekday()]
			if showtime is not None:
				presentation = STPresentation()
				presentation.date = datetime.datetime.combine(single_date,showtime)
				presentation.day  = datetime.datetime.combine(single_date.date(),datetime.time())
				presentation.time = showtime
				presentation.season = season.key()
				logging.debug("Will schedule a presentation for" + str(presentation.date))
				presentation.put()

		self.set_flash('Se ha creado el montaje, la temporada y las presentaciones que pediste')
		self.redirect('/admin/montages/'+montage.slug)
		

		


