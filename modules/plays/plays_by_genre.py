#!/usr/bin/env python
#
from lib.imports import *


class PlaysByGenre(llhandler.LLHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def get(self, genre):
		self.internal_get()

	def internal_get(self):
		self.render('index',template_values={})

