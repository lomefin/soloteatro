#!/usr/bin/env python
#
from lib.imports import *


class PresentationList(llhandler.LLHandler):
	def base_directory(self):
		return os.path.dirname(__file__)


	def internal_get(self):


		open_seasons = STSeason.all().filter("status = ","Open")
		
		self.set("open_seasons",open_seasons)
		self.set("thumb_sizes",[3,4,5])
		self.render('list_presentations')
