from lib.imports import *

class AddVenue(llhandler.LLGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		self.render('/admin/add_venue',template_values={})

	def internal_post(self):

		venue = STVenue()
		venue.name = self.param('venue_name')
		venue.address = self.param('venue_address')
		venue.telephone = self.param('venue_telephone')
		venue.url = self.param('venue_url')
		venue.parking = self.param('venue_parking')
		venue.twitter = self.param('venue_twitter')
		venue.facebook = self.param('venue_facebook')
		
		logging.debug("Put on object")
		key = venue.put()
		time.sleep(1)
		venue = STVenue.get(key)
		self.redirect('/admin/venues/'+str(venue.slug))

class ViewVenue(llhandler.LLGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def transitional_get(self,args):
		self.internal_get(venue_code = args[0])

	def internal_get(self,venue_code):
		logging.debug("Looking for " + venue_code)
		venue = STVenue.all().filter('slug =',venue_code).get()
		self.render('/admin/view_venue',template_values={'venue':venue})