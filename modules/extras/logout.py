#!/usr/bin/env python
#

#!/usr/bin/env python
#
from lib.imports import *



class Logout(STHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)


	def internal_get(self):
		self.session.terminate()
		self.logout_url = users.create_logout_url('/')
		self.redirect(self.logout_url)
	
