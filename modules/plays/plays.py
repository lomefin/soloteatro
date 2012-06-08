#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
from modules.plays.plays_by_genre import *


			

def main():
  LLApp([('/obras/genero/([a-zA-Z]*)', PlaysByGenre),],debug=True)
  #application = webapp.WSGIApplication([('/obras/genero/([a-zA-Z]*)', PlaysByGenre),
  #										('.*',lib.errors.NotFoundHandler),
  #										],
  #                                     debug=True)
  #util.run_wsgi_app(application)


#if __name__ == '__main__':
#  main()


# def main():
#   application = webapp.WSGIApplication([('/obras/', PlayHandler),
#   										('/obras/proponer/',NewPlayHandler),
#   										('/obras/_new',NewPlayHandler),
#   										('/obras/([a-zA-Z\-0-9]*)',ViewPlayHandler),
# 										('/obras/([a-zA-Z\-0-9]*)/edit',EditPlayHandler),
# 										('/obras/generos',CategoryHandler),
# 										('/obras/genero/([a-zA-Z]*)',CategoryHandler),
# 										('.*',lib.errors.NotFoundHandler)],
#                                        debug=True)

# class PlayHandler(llhandler.LLHandler):
	
# 	def base_directory(self):
# 		return os.path.dirname(__file__)
	
# 	def internal_get(self):
# 		offset = 0
# 		try:
# 			if(self.request.get('offset') is not None):
# 				offset=int(self.request.get('offset'))
# 		except:
# 			pass
# 		if LLPlay.all().count() > 0:
# 			articles = LLPlay.all().order('-date_created').fetch(10,offset)
# 			for article in articles:
# 				article.markdown_html = markdown2.markdown(article.synopsis,extras={"code-friendly":None,"html-classes":{"pre":"prettyprint"}})
# 			values = {'articles':articles,'offset':offset+10,'is_offset':len(articles)>10}
# 			self.render('index',template_values=values)
# 		else:
# 			self.render('index')
	

# class NewPlayHandler(llhandler.LLGAEHandler):
# 	def base_directory(self):
# 		return os.path.dirname(__file__)

# 	def internal_get(self):

# 		self.render('propose_play')
	
# 	def internal_post(self):
# 		try:
# 			play = LLPlay()
# 			play.title = self.request.get('title')
# 			play.synopsis = self.request.get('content')
# 			play.creator = self.current_account
# 			play.possible_slug = play.title + "2012-02"
# 			play.put()
# 			if self.request.get('publish') != "true":
# 			  message.is_active = False
# 			  message.put()
# 			else:
# 			  self.set_flash('La propuesta de obra ha sido agregada')
# 		except :
# 			self.set_flash('No se pudo agregar la propuesta obra.',flash_type='errorFlash')

			
# 		self.redirect('/obras/')
	

# class ViewPlayHandler(llhandler.LLHandler):
# 	def base_directory(self):
# 		return os.path.dirname(__file__)
		
# 	def get(self,slug):
# 		self.auth_check()
# 		self.view_post(slug)
		
# 	def view_post(self,slug):
# 		post = LLPlay.all().filter('slug =',slug).get()

# 		if post is not None:
# 			markdown_html = markdown2.markdown(post.synopsis,extras={"code-friendly":None,"html-classes":{"pre":"prettyprint"}})
# 			values = {'post':post,'from':self.request.path,'markdown_html':markdown_html}
# 			self.render('view_post',template_values=values)
# 		else:
# 			self.set_flash('No existe esa obra',flash_type='errorFlash')
# 			self.redirect('/obras/')

# class EditPlayHandler(llhandler.LLGAEHandler):
# 	def base_directory(self):
# 		return os.path.dirname(__file__)
		
# 	def get(self,slug):
# 		self.auth_check()
# 		self.view_post(slug)
		
# 	def view_post(self,slug):
# 		post = LLPlay.all().filter('slug =',slug).get()
	
# 		if post is not None:
# 			markdown_html = markdown2.markdown(post.text,extras={"code-friendly":None,"html-classes":{"pre":"prettyprint"}})
# 			values = {'post':post,'from':self.request.path,'markdown_html':markdown_html}
# 			self.render('edit_post',template_values=values)
# 		else:
# 			self.set_flash('No existe ese post',flash_type='errorFlash')
# 			self.redirect('/posts/')
			
# 	def post(self,slug):
# 		self.auth_check()
# 		self.edit_post(slug)
	
# 	def edit_post(self,slug):
# 		post = LLPlay.all().filter('slug =',slug).get()
# 		#post = LLArticle.get_by_id(int(post_id))
# 		if post is not None:
# 			post_body = self.request.get('content')
# 			post.text = post_body
# 			post.put()
# 			self.set_flash('Cambios agregados',flash_type='successFlash')
# 			self.view_post(slug)
			
# 			return
# 		else:
# 			self.set_flash('No existe esa obra',flash_type='errorFlash')

#			self.redirect('/obras/')