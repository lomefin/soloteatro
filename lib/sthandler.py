from lib.imports import *


class STHandler(llhandler.LLHandler):
	
	def get(self,*args):
		self.auth_check()

		new_args = []
		for arg in args:
			new_args.append(str(arg))
		args = new_args
		self.show_actives_genres_in_menu()
		self.transitional_get(args)
	
	def post(self,*args):
		self.auth_check()

		new_args = []
		for arg in args:
			new_args.append(str(arg))
		args = new_args
		self.show_actives_genres_in_menu()
		self.transitional_post(args)

	def show_actives_genres_in_menu(self):

		#Optimization for current presentations, use when DB load goes up.
		# if(self.session):
		# 	if(self.session.has_key('active_genres')):
		# 		self.set('active_genres',self.session['active_genres'])
		# 		logging.debug("Active Genres List Recycled")
		# 	if (self.session.has_key('active_seasons')):
		# 		self.set('active_seasons',self.session['active_seasons'])
		# 		return	



		active_seasons = db.GqlQuery("SELECT * FROM STSeason WHERE status = 'Open' ORDER BY genre")
		active_genres = {}
		for season in active_seasons:

			active_genres[season.genre] = True

		self.set("active_genres",active_genres)
		logging.debug("Active Genres List Generated")
		if(self.session):
			self.session['active_genres'] = active_genres
			self.session['active_seasons'] = active_seasons
