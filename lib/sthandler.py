from lib.imports import *


class STHandler(llhandler.LLHandler):

	def get(self,*args):
		logging.debug("STH.get")
		self.auth_check()

		new_args = []
		for arg in args:
			new_args.append(str(arg))
		args = new_args
		self.show_actives_genres_in_menu()
		self.show_presentations_on_calendar()
		self.transitional_get(args)
	
	def post(self,*args):
		self.auth_check()

		new_args = []
		for arg in args:
			new_args.append(str(arg))
		args = new_args
		self.show_actives_genres_in_menu()
		self.show_presentations_on_calendar()
		self.transitional_post(args)



	def calculate_presentations_on_calendar(self):
		calendar_start_date = datetime.date.today() - datetime.timedelta(days = datetime.date.today().isoweekday()-1)
		calendar_end_date = calendar_start_date + datetime.timedelta(weeks=4)
		calendar_end_date = calendar_end_date + datetime.timedelta(days = 7 - calendar_end_date.isoweekday())

		return self.calculate_presentations_on_dates(start_date=calendar_start_date,end_date=calendar_end_date)
	
	def get_presentations_on_dates(self,start_date,end_date):
		current_date = start_date
		days = []
		self.logger.info("Getting presentations from {start} to {end}".format(start=start_date,end=end_date))
		while(current_date <= end_date):
			presentations_that_day = STPresentation.all().filter('day =',current_date)
			if presentations_that_day.count(1)> 0 :
				day_presentations = dict(map(lambda x: [x.season.montage.name,x],presentations_that_day))
				
				days.append({'date':current_date, 'presentations':day_presentations.values(),
							'date_string':current_date.strftime("%Y-%m-%d")})
			current_date = current_date +datetime.timedelta(days=1)
			#self.logger.debug("Current day count for {day} is {count}".format(day=current_date,count=presentations_that_day.count(10)))
		return days

	def calculate_presentations_on_dates(self,start_date,end_date):	
		current_date = start_date
		month_weeks = []
		current_month = datetime.date.today().month
		self.logger.info("calculate_presentations_on_dates " + str(start_date)+" thru "+ str(end_date))
		while(current_date <= end_date):
			week = []
			for i in range(7):
				current_day = {'day':current_date.day,'date_string': current_date.strftime("%Y-%m-%d"),'current_month':current_month == current_date.month}
				presentations_that_day = STPresentation.all().filter('day =',current_date)
				current_day['is_today'] = current_date == datetime.date.today()
				if presentations_that_day.count(1) > 0:
					current_day['has_shows'] = 1
				current_date = current_date +datetime.timedelta(days=1)
				week.append(current_day)
			month_weeks.append(week)
		return month_weeks

	def show_presentations_on_calendar(self):
		

		if self.session: #While there is low load.
			if not self.session.has_key('calendar_presentations'):
				self.session['calendar_presentations'] = self.calculate_presentations_on_calendar()
			self.set("calendar_presentations",self.session['calendar_presentations'])
		else:
			self.set("calendar_presentations",self.calculate_presentations_on_calendar())

	def show_actives_genres_in_menu(self):

		#Optimization for current presentations, use when DB load goes up.
		#if(self.session):
		#	if(self.session.has_key('active_genres')):
		#		self.set('active_genres',self.session['active_genres'])
		#		logging.debug("Active Genres List Recycled")
		#	if (self.session.has_key('active_seasons')):
		#		self.set('active_seasons',self.session['active_seasons'])
		#		return	

		genres = STGenre.all().order('rating')
		active_genres = []
		active_seasons = []
		for genre in genres:
			open_seasons_query = genre.seasons.filter('status = ', 'Open')
			if open_seasons_query.count() > 0:
				active_genres.append(genre)
				active_seasons.append(open_seasons_query.fetch(100))


		self.set("active_genres",active_genres)
		if(self.session):
			self.session['active_genres'] = active_genres
			self.session['active_seasons'] = active_seasons
