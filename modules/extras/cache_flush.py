#!/usr/bin/env python
#
from lib.imports import *


class CacheFlush(STHandler):
	def base_directory(self):
		return os.path.dirname(__file__)


	def internal_get(self):
		self.session.clear()

		self.set_flash("Cache limpiada")
		logging.debug("Cache cleared")

		self.redirect("/")
