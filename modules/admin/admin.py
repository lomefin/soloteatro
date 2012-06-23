from lib.imports import *
from modules.admin.plays import *
from modules.admin.venues import *
from modules.admin.montages import *
from modules.admin.seasons import *

def main():
  LLApp([
  		('/admin/montages/add', AddMontage),
  		('/admin/montages/', ListMontages),
  		('/admin/montages/(.*)/seasons/add',AddSeasonToMontage),
  		('/admin/montages/(.*)',ViewMontage),
  		('/admin/seasons/add',AddSeason),
      ('/admin/seasons/express_add',AddSeasonExpress),
  		('/admin/plays/add', AddPlay),
  		('/admin/venues/add', AddVenue),
  		('/admin/venues/(.*)', ViewVenue),])

if __name__ == "__main__":
  main()