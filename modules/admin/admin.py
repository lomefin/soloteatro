from lib.imports import *
from modules.admin.plays import *
from modules.admin.theatres import *


def main():
  application = webapp.WSGIApplication([('/admin/plays/add', AddPlay),
  										('/admin/venues/add', AddVenue),
  										('/admin/venues/(.*)', ViewVenue),
  										('.*',lib.errors.NotFoundHandler),
  										],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()