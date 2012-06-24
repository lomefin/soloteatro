#!/usr/bin/env python
#
from lib.imports import *


class PresentationsByGenre(llhandler.LLHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def transitional_get(self, args):
		self.internal_get(genre=args[0])

	def internal_get(self,genre):

		logging.debug("Showing presentations of " + genre)
		current_shows = STSeason.all().filter("status = ","open").filter("genre = ",genre)
		self.set("genre",genre)
		self.set("current_shows",current_shows)

		self.render('presentations_of_genre')
