#!/usr/bin/env python
#

#!/usr/bin/env python
#
from lib.imports import *



class DisplayPicture(STHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)

	def transitional_get(self, args):

		self.internal_get(args[0])

	def internal_get(self,image_id):
		self.logger.debug("Getting image")
		self.logger.debug(image_id)

		stimage = None
		stimage = STImage.get(db.Key(encoded=image_id))
		self.logger.info(stimage)
		if stimage:
			if stimage.payload:
				self.response.headers['Content-Type'] = "image/png"
				self.response.out.write(stimage.payload)
        #if stimage.payload:
        #    self.response.headers['Content-Type'] = "image/png"
        #    self.response.out.write(stimage.payload)
        #else:
        #    self.error(404)
		
	
