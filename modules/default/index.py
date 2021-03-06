#!/usr/bin/env python
#
# Copyright 2012 Leonardo Luarte, 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from lib.imports import *

class DefaultHandler(STHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		seasons = []
		rand_seasons = db.GqlQuery("SELECT * FROM STSeason WHERE status = 'Open' ORDER BY last_shown ASC LIMIT 3 ")
		for season in rand_seasons:
			selected_media = None
			season.last_shown = datetime.datetime.now()
			season.put()
			for media in season.related_media:
				if media.selected:
					selected_media = media
			seasons.append({'season':season,'selected_media':selected_media})
		latest_articles = db.GqlQuery("SELECT * FROM STArticle ORDER BY date_created DESC LIMIT 4")
		self.set("latest_articles",latest_articles)
		self.set("rand_seasons",seasons)
		self.render('default/index')

class IndexHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write('index')

application = LLApp([('/', DefaultHandler)]).application
