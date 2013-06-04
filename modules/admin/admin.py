from lib.imports import *
from modules.admin.plays import *
from modules.admin.venues import *
from modules.admin.montages import *
from modules.admin.seasons import *
from modules.admin.media import *
from modules.admin.reports import *
from modules.admin.genres import *
from modules.admin.articles import *

application = LLApp([
      ('/admin/montages/new', NewMontage),
      ('/admin/montages/', ListMontages),
      ('/admin/montages/(.*)/seasons/add',AddSeasonToMontage),
      ('/admin/montages/(.*)/season/(\d*)/media/add',AddMediaToSeason),
      ('/admin/montages/(.*)/(pictures|videos)/add',AddMediaToLatestSeason),
      ('/admin/media/(.*)/toggle',ToggleMediaSelection),
      ('/admin/montages/(.*)',ViewMontage),
      ('/admin/seasons/add',AddSeason),
      ('/admin/seasons/express_add',AddSeasonExpress),
      ('/admin/plays/add', AddPlay),
      ('/admin/venues/add', AddVenue),
      ('/admin/venues/(.*)', ViewVenue),
      ('/admin/media/video/(\S*)',AddVideoToSeason),
      ('/admin/media/image/(\S*)',AddPictureToSeason),
      ('/admin/genres/',AdminGenres),
      ('/admin/articles/',AdminArticles),
      ('/admin/',ShowReports),
      ]).application