
from lib.imports import *

class AddSeason(llhandler.LLGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		self.render('/admin/add_montage',template_values={})

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
		self.set('value_list', STVenue.all())
		self.render('/admin/add_season')

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
		self.set('montages',STMontage.all().order('-date_created').fetch(100))
		self.set('genres',STGenre.all().order('rating'))
		self.render('/admin/add_season_express',template_values={'venue_list':venue_list})

	def daterange(self,start_date, end_date):
		logging.debug(start_date)
		logging.debug(end_date)
		for n in range((end_date - start_date).days):
			yield start_date + timedelta(n)

	def internal_post(self):
		
		genre = STGenre.all().filter('slug =',self.param('montage_genre')).get()
		#The Montage
		montage = STMontage()
		montage.name = self.param('montage_name')
		montage.director = self.param('montage_director')
		montage.writer	= self.param("montage_writer")
		montage.genre = genre
		montage.description = self.param('montage_description')
		montage.company = self.param('montage_company')
		montage.slug = Slugger.slugify(montage.name + " de "+montage.director)
		montage.put()
		
		seasons_for_this_montage = montage.seasons.count()
		
		venue = None
		
		if self.param('venue_name'):
			logging.info("Venue does not exists")
			venue = STVenue()
			venue.name = self.param('venue_name')
			venue.address = self.param('venue_address')
			venue.put()

		if not venue:
			logging.info("Choosing existing venue")
			logging.info(self.param("season_venue"))
		#The first season
		season = STSeason()
		season.montage = montage.key()
		logging.info(self.param("season_venue"))
		if venue:
			season.venue = venue 
		else:
			season.venue = db.Key(encoded = self.param("season_venue"))
		season.start = datetime.datetime.strptime(self.param("season_start"),"%d/%m/%Y")
		season.end = datetime.datetime.strptime(self.param("season_end"),"%d/%m/%Y")
		season.repetition = seasons_for_this_montage + 1
		season.status = db.Category("Open")
		season.cast = self.param("season_cast").split(",")
		season.technical_team = self.param("season_technical_team").split(",")
		season.prices = self.param("season_prices").split(",")
		season.genre = montage.genre
		season.put()
		#Le Plays for that season
		showtimes_week = []
		for (idx,day) in enumerate(['monday','tuesday','wednesday','thursday','friday','saturday','sunday']):
			showtimes_week.insert(idx,[])
			for i in range(1,3):
				logging.debug("Checking " + 'plays_on_'+day+ ">> " + self.param('plays_on_'+day))
				logging.debug(self.param(day + '_showtime_'+str(i)))
				if self.param('plays_on_'+day):
					showtimes_week[idx].append(datetime.datetime.strptime(self.param(day + '_showtime_'+str(i)),"%H:%M").time())
		logging.info(showtimes_week)
		
		for single_date in self.daterange(season.start, season.end):
			showtimes = showtimes_week[single_date.weekday()]
			last_showtime = ""
			for showtime in showtimes:
				if last_showtime == showtime:
					continue
				presentation = STPresentation()
				presentation.date = datetime.datetime.combine(single_date,showtime)
				presentation.day  = datetime.datetime.combine(single_date.date(),datetime.time())
				presentation.time = showtime
				presentation.season = season.key()
				logging.debug("Will schedule a presentation for" + str(presentation.date))
				presentation.put()
				last_showtime = showtime

		self.set_flash('Se ha creado el montaje, la temporada y las presentaciones que pediste')
		self.redirect('/admin/montages/'+montage.slug)
		

		


