#!/usr/bin/env python
#
from lib.imports import *


class UpdateSeasons(STHandler):
  def base_directory(self):
    return os.path.dirname(__file__)


  def internal_get(self):
    open_seasons = STSeason.all().filter("status = ","Open")

    for season in open_seasons:
      logging.debug (str(season.end))
      if season.end < datetime.now:
        season.status = db.Category("Closed")
        season.put()

    self.redirect('/admin/')
