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
		current_season = montage.seasons.order('repetition').get()
		
		selected_media = None
		for media in current_season.related_media:
			if media.selected:
				selected_media = media
		#current_season = seasons[0]
		today = datetime.datetime.now()
		next_week = today + datetime.timedelta(weeks=1)
		future_presentations = []
		for presentation in current_season.presentations:
			if (today <= presentation.date <= next_week):
					future_presentations.append(presentation)
		

		self.set("future_presentations",future_presentations)
		self.set("season",current_season)
		self.set("montage",current_season.montage)
		self.set("selected_media",selected_media)
		self.render('view_presentation')
