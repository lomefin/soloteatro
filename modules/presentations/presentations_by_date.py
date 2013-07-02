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
		
		start = start_date - timedelta(days=2)
		end = end_date + timedelta(days=2)
		days = self.get_presentations_on_dates(start_date=start,end_date=end)

		self.set("start",start)
		self.set("original_start",start_date)
		self.set("end",end)
		self.set("days",days)

		self.render('presentations/presentations_of_date')