#!/usr/bin/env python
#
from lib.imports import *


class PresentationsByGenre(STHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def transitional_get(self, args):
		self.internal_get(genre=args[0])

	def internal_get(self,genre):

		logging.debug("Showing presentations of " + genre)

		open_seasons = STSeason.all().filter("status = ","Open").filter("genre = ",genre)
		
		self.set("genre",genre)
		self.set("open_seasons",open_seasons)

		self.render('presentations_of_genre')
