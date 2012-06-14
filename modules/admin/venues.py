from lib.imports import *

class AddVenue(llhandler.LLHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		self.render('add_venue',template_values={})

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

class ViewVenue(llhandler.LLHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def get(self,venue_code):
		self.internal_get(venue_code)

	def internal_get(self,venue_code):
		logging.debug("Looking for " + venue_code)
		venue = STVenue.all().filter('slug =',venue_code).get()
		self.render('view_venue',template_values={'venue':venue})