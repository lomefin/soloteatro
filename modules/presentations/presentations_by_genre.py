#!/usr/bin/env python
#
from lib.imports import *


class PresentationsByGenre(STHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def transitional_get(self, args):
		self.internal_get(genre_slug=args[0])

	def internal_get(self,genre_slug):

		genre = STGenre.all().filter('slug = ',genre_slug).get()

		logging.debug("Showing presentations of " + genre.name)

		open_seasons = genre.seasons.filter("status = ","Open")
		
		self.set("genre",genre)
		self.set("open_seasons",open_seasons)

		self.render('presentations/presentations_of_genre')
