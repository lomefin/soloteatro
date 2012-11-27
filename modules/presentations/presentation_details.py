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
		
		selected_media = current_season.related_media.order('-priority').get()
		pictures = current_season.related_media.filter('class = ','STPicture')
		today = datetime.datetime.now()
		next_2_weeks = today + datetime.timedelta(weeks=2)
		future_presentations = []
		for presentation in current_season.presentations:
			logging.debug("Presentations: "+ str(presentation))
			if (today <= presentation.date <= next_2_weeks):
					future_presentations.append(presentation)
					logging.debug("Appending " + str(presentation))
		

		self.set("future_presentations",future_presentations)
		self.set("season",current_season)
		self.set("montage",current_season.montage)
		self.set("selected_media",selected_media)
		self.set('pictures',pictures)
		self.render('view_presentation')
