from lib.imports import *


class STHandler(llhandler.LLHandler):
	

	def get(self,*args):
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
		current_month = datetime.date.today().month
		self.logger.info("Getting presentations from {start} to {end}".format(start=start_date,end=end_date))
		while(current_date <= end_date):
			
			current_day = {'day':current_date.day,'current_month':current_month == current_date.month}
			presentations_that_day = STPresentation.all().filter('day =',current_date)
			days.append(presentations_that_day)
			current_date += datetime.timedelta(days=1)
		return days

	def calculate_presentations_on_dates(self,start_date,end_date):	
		current_date = start_date
		month_weeks = []
		current_month = datetime.date.today().month
		self.logger.info("Calculation presentations for caledar")
		while(current_date <= end_date):
			week = []
			for i in range(7):
				current_day = {'day':current_date.day,'current_month':current_month == current_date.month}
				presentations_that_day = STPresentation.all().filter('day =',current_date)
				if presentations_that_day.count(1) > 0:
					current_day['has_shows'] = 1
				current_date += datetime.timedelta(days=1)
				week.append(current_day)
			month_weeks.append(week)
		return month_weeks

	def show_presentations_on_calendar(self):
		

		if self.session and False: #While there is low load.
			if not self.session['calendar_presentations']:
				self.session['calendar_presentations'] = self.calculate_presentations_on_calendar()
			self.set("calendar_presentations",self.session['calendar_presentations'])
		else:
			self.set("calendar_presentations",self.calculate_presentations_on_calendar())

	def show_actives_genres_in_menu(self):

		#Optimization for current presentations, use when DB load goes up.
		# if(self.session):
		# 	if(self.session.has_key('active_genres')):
		# 		self.set('active_genres',self.session['active_genres'])
		# 		logging.debug("Active Genres List Recycled")
		# 	if (self.session.has_key('active_seasons')):
		# 		self.set('active_seasons',self.session['active_seasons'])
		# 		return	



		active_seasons = db.GqlQuery("SELECT * FROM STSeason WHERE status = 'Open' ORDER BY genre")
		active_genres = {}
		for season in active_seasons:

			active_genres[season.genre] = True

		self.set("active_genres",active_genres)
		logging.debug("Active Genres List Generated")
		if(self.session):
			self.session['active_genres'] = active_genres
			self.session['active_seasons'] = active_seasons
