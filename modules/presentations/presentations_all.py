#!/usr/bin/env python
#
from lib.imports import *


class PresentationList(STHandler):
	def base_directory(self):
		return os.path.dirname(__file__)


	def internal_get(self):


		open_seasons = STSeason.all().filter("status = ","Open")
		
		self.set("open_seasons",open_seasons)
		self.set("thumb_sizes",[3,4,5])
		self.set("thumb_rotations",[-10,-7,-4,-2,3,6,11])
		self.render('list_presentations')
