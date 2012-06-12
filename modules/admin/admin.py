from lib.imports import *
from modules.admin.plays import *
from modules.admin.venues import *
from modules.admin.montages import *

def main():
  LLApp([
  		('/admin/montages/add', AddMontage),
  		('/admin/montages/', ListMontages),
  		('/admin/montages/(.*)',ViewMontage),
  		('/admin/plays/add', AddPlay),
  		('/admin/venues/add', AddVenue),
  		('/admin/venues/(.*)', ViewVenue),])

