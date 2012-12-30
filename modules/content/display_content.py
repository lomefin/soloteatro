#!/usr/bin/env python
#

#!/usr/bin/env python
#
from lib.imports import *



class DisplayContent(STHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)

	def transitional_get(self, *args):
		if args[0][0] == 'links':
			self.render('links')
		else:
			self.render('index')

	def internal_get(self):
		self.render('index',template_values={})
	
