from lib.imports import *
from modules.admin.plays import *
from modules.admin.venues import *
from modules.admin.montages import *
from modules.admin.seasons import *
from modules.admin.media import *
from modules.admin.reports import *
def main():
  LLApp([
  		('/admin/montages/add', AddMontage),
  		('/admin/montages/', ListMontages),
  		('/admin/montages/(.*)/seasons/add',AddSeasonToMontage),
  		('/admin/montages/(.*)/season/(\d*)/media/add',AddMediaToSeason),
      ('/admin/montages/(.*)/pictures/add',AddMediaToLatestSeason),
      ('/admin/montages/(.*)',ViewMontage),
  		('/admin/seasons/add',AddSeason),
      ('/admin/seasons/express_add',AddSeasonExpress),
  		('/admin/plays/add', AddPlay),
  		('/admin/venues/add', AddVenue),
  		('/admin/venues/(.*)', ViewVenue),
      ('/admin/media/video/(\S*)',AddVideoToSeason),
      ('/admin/',ShowReports),
      ])

if __name__ == "__main__":
  main()