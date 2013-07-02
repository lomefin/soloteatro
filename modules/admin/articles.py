from lib.imports import *

class AdminArticles(llhandler.LLGAEHandler):
  def base_directory(self):
    return os.path.dirname(__file__)

  def internal_get(self):
    latest_articles = STArticle.all().order('date_created').fetch(10)
    self.set('latest_articles',latest_articles)
    self.render('/admin/admin_article')

  def internal_post(self):
    article = STArticle()
    article.title = self.param("article_title")
    article.body  = self.param("article_body")
    new_article = article.put()

    if not new_article:
      self.set_flash('Hubo un problema agregando el articulo.')
    else:
      self.set_flash("Articulo agregado")

    self.internal_get()



class ListArticles(llhandler.LLGAEHandler):
  def base_directory(self):
    return os.path.dirname(__file__)
  
  def internal_get(self):

    self.render('/admin/dashboard')
    
