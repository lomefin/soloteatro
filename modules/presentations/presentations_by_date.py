#!/usr/bin/env python
#
from lib.imports import *


class PresentationsToday(STHandler):
	def base_directory(self):
		return os.path.dirname(__file__)

	def internal_get(self):

		logging.debug("Showing presentations of today ")

		presentations_that_day = self.get_presentations_on_dates(start_date=datetime.date.today(),end_date=datetime.date.today())
		
		self.set("days",presentations_that_day)
		
		self.render('presentations_of_today')

class PresentationsInTimeSpan(STHandler):

	def base_directory(self):
		return os.path.dirname(__file__)
	def transitional_get(self, args):
		self.internal_get(date_from=args[0],date_to=args[1])

	def internal_get(self,date_from,date_to):
		start_date=dparser.parse(date_from,fuzzy=True)
		end_date=dparser.parse(date_to,fuzzy=True)
		#logging.debug("Showing presentations from {start} to {end} ".format(start=date_from,end=date_to))
		#logging.debug("Showing presentations from {start} to {end} ".format(start=start_date,end=end_date))

		days = self.get_presentations_on_dates(start_date=start_date,end_date=end_date)
		
		self.set("start",start_date)
		self.set("end",end_date)
		self.set("days",days)

		self.render('presentations_of_date')