#!/usr/bin/env python
#
from lib.imports import *


class ViewVenue(STHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def transitional_get(self,args):
		self.internal_get(venue_code = args[0])

	def internal_get(self,venue_code):
		logging.debug("Looking for " + venue_code)
		venue = STVenue.all().filter('slug =',venue_code).get()
		self.render('venues/view_venue',template_values={'venue':venue})
