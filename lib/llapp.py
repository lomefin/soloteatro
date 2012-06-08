#!/usr/bin/env python
#
# Copyright 2012 Leonardo Luarte.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from lib.imports import *



class LLApp():
	def __init__(self,routes=[],debug=True):
		
		logging.getLogger().setLevel(logging.DEBUG)

		default_routes = [('.*',lib.errors.NotFoundHandler),]

		routes.extend(default_routes)

		application = webapp.WSGIApplication(routes,debug=debug)

  		util.run_wsgi_app(application)
