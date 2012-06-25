#!/usr/bin/env python
#
from lib.imports import *


class PresentationDetails(STHandler):
	def base_directory(self):
		return os.path.dirname(__file__)

	def transitional_get(self,args):

		self.internal_get(montage_slug = args[0])

	def internal_get(self,montage_slug):

		montage = STMontage.all().filter("slug =",montage_slug).get()
		
		seasons = sorted(montage.seasons , key=lambda season: season.repetition)

		current_season = seasons[0]


		self.set("season",current_season)
		self.set("montage",current_season.montage)
		self.render('view_presentation')
