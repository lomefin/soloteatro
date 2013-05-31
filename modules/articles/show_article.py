#!/usr/bin/env python
#
from lib.imports import *


class ShowArticle(STHandler):
	def base_directory(self):
		return os.path.dirname(__file__)

	def transitional_get(self,args):

		self.internal_get(article_slug = args[0])

	def internal_get(self,article_slug):

		article = STArticle.all().filter("slug =", article_slug).get()
		
		self.set("article",article)
		self.render('articles/show_article')
