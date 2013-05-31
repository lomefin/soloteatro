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

    #Setting up logging   
    logging.getLogger().setLevel(logging.DEBUG)

    def handle_404(self,request, response, exception):
        logging.exception(exception)
        logging.error('Oops! I could swear this page was here!')
        response.set_status(404)

    def handle_500(self,request, response, exception):
        logging.exception(exception)
        logging.error('A server error occurred!')
        response.set_status(500)

    #Setting routes and launching
    default_routes = [('.*',lib.errors.NotFoundHandler),]
    routes.extend(default_routes)
    self.application = webapp2.WSGIApplication()

    all_routes = []
    for route in routes:
      self.application.router.add(route)

