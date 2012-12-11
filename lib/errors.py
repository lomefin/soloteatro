#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
from lib import llhandler
import templates
from root_dir import root_directory
class NotFoundHandler(llhandler.LLHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def get(self):
		template_values = {}
		print root_directory()
		jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(root_directory()+'/templates/'),cache_size=0)
		print jinja_environment
		template = jinja_environment.get_template('error.html')
		print template
		self.response.write(template.render(template_values)) 
		self.response.set_status(404)

	def post(self):
		self.get()

	def render_specific(self,pagename,template_values=None):
		#self.wr(os.path.dirname(__file__))
		path = os.path.join(self.base_directory(), pagename+'.html')
		#self.wr(path)
		self.response.out.write(template.render(path, template_values))
		