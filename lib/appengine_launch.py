

import os
from google.appengine.dist import use_library
#Setting up django
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
use_library('django', '1.2')

from django.conf import settings
_ = settings.TEMPLATE_DIRS

