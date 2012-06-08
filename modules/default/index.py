
from lib.imports import *

class DefaultHandler(llhandler.LLHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		
		
		
		self.render('index',template_values={})

class NotFoundHandler(llhandler.LLHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def get(self):
		self.render('not_found')

def main():
  application = webapp.WSGIApplication([('/', DefaultHandler),('/.*',NotFoundHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
