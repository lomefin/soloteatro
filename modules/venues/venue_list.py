#!/usr/bin/env python
#
from lib.imports import *


class ListVenues(STHandler):
  def base_directory(self):
    return os.path.dirname(__file__)
  
  def internal_get(self):
    venues = STVenue.all()
    self.set('venues',venues)
    self.render('venues/list_venues')
