#!/usr/bin/env python
#
from lib.imports import *


class PresentationList(llhandler.LLHandler):
	def base_directory(self):
		return os.path.dirname(__file__)


	def internal_get(self):


		open_seasons = STSeason.all().filter("status = ","Open")
		
		self.set("open_seasons",open_seasons)

		self.render('presentations_of_genre')
