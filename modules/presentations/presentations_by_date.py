#!/usr/bin/env python
#
from lib.imports import *


class PresentationsToday(STHandler):
	def base_directory(self):
		return os.path.dirname(__file__)

	def internal_get(self):

		logging.debug("Showing presentations of today ")

		presentations_that_day = self.get_presentations_on_dates(start_date=datetime.date.today(),end_date=datetime.date.today())
		
		self.set("presentations",presentations_that_day)
		
		self.render('presentations_of_today')

class PresentationsInTimeSpan(STHandler):

	def transitional_get(self, args):
		self.internal_get(date_from=args[0],date_to=args[1])

	def internal_get(self,date_from,date_to):

		logging.debug("Showing presentations from {start} to {end} ".format(start=date_from,end=date_to))

		presentations = self.get_presentations_on_dates(start_date=date_from,end_date=date_to)
		
		self.set("presentations",presentations)

		self.render('presentations_of_date')