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



class LLDefaultHandler(webapp.RequestHandler):
	def __init__(self):
		self.flash = None
		self.flash_type = 'success'
		self.log_count = 1
		self.values = {}
		self.logger = logging.getLogger(__name__)
		#self.auth_check()
	
	def set_flash(self,flash,flash_type='info'):
		if(self.session):
			self.session['flash'] = flash
			self.session['flash_type'] = flash_type
	
	def read_flash(self):
		if(self.session):
			if(self.session.has_key('flash')):
				self.flash = self.session.pop('flash',default=None)
				self.flash_type = self.session.pop('flash_type',default='success')
			
	
	def auth_check(self):
		
		self.session = get_current_session()
		user = users.get_current_user()
		self.current_account = None
			
		if(user and self.session):
			if self.session.has_key("current_account"):
				self.current_account = self.session["current_account"]	
			else:
				self.current_account = STAccount.all().filter('email = ',user.email()).get()
				
				if not self.current_account:
					self.current_account = STAccount()
					self.current_account.email = user.email()
						#self.current_account.put()
					#Setting the session data
				#self.current_account.is_administrator = users.is_current_user_admin()
				self.current_account.last_entrance = datetime.datetime.now()
				self.current_account.put()
				self.session["current_account"] = self.current_account
				
				time.sleep(1)
		
		else:
			self.login_url = users.create_login_url('/')
		
		
		return True

	def set(self,key,value):

		if not self.values:
			self.values = {}
		self.values[key] = value

	def error404(self):

		template_values = {}
		logging.warn("Invokking error 404.  base_directory = " + str(self.base_directory()))

		
		path = os.path.join(settings.TEMPLATE_DIRS, 'not_found.html')
		template_file = open(path) 
		compiled_template = template.Template(template_file.read()) 
		template_file.close()  
		self.response.out.write(compiled_template.render(template.Context(template_values)))

		
		self.response.set_status(404)
			
	def render(self,pagename,template_values=None):
		
		if not template_values:
			template_values = self.values
			
		try:
			self.read_flash()
			
			template_values['flash'] = self.flash
			template_values['flash_type'] = self.flash_type
			
			if self.current_account:
				template_values['logged_user'] = self.current_account
			if self.login_url:
				template_values['login_url'] = self.login_url
			if self.session.has_key("current_account"):
				template_values['logged_user'] = self.session["current_account"]
			if self.logout_url:
				template_values['logout_url'] = self.logout_url
			
		except:
			pass
		
		path = os.path.join(self.base_directory(), 'views/'+pagename+'.html')
		template_file = open(path) 
		compiled_template = template.Template(template_file.read()) 
		template_file.close()  
		self.response.out.write(compiled_template.render(template.Context(template_values)))
		
	def base_directory(self):
		return os.path.dirname(__file__)

	def render_specific(self,pagename,template_values=None):
		#self.wr(os.path.dirname(__file__))
		path = os.path.join(self.base_directory(), pagename)
		#self.wr(path)
		self.response.out.write(template.render(path, template_values))
	
	def wr(self,text):
		self.response.out.write(text)
		
	def log(self,text,type="info"):
		color = "white"
		if(type == "error"): color="aa5555"
		elif(type == "warn"): color="orange"
		elif(type == "ok"): color="#55aa55"
		
		self.wr('<p style="background-color:'+color+'"><span class="operationNumber" style="min-width:50px">'+str(self.log_count)+'</span>'+text+'</p>')
		self.log_count = self.log_count + 1
	def param(self,param_name):
		return self.request.get(param_name)

	def param_dump(self):

		logging.debug("Parameter dump")
		for arg in self.request.arguments():
			logging.debug("|" +str(arg))
			for element in self.request.get_all(arg):
				logging.debug("---" + str(element))

	def retrieve_or_404(self,data):
		if data is not None:
			logging.debug("Data is not None")
			return data

		logging.info("The requested data is None, sending 404 error.")	
		#self.error404()
	
	def get_or_404(self,data):

		logging.warn("Deprecated method, use retrieve_or_404")
		return self.retrieve_or_404(data)

	#This one is in charge of moving from *args to named params, if needed
	def transitional_get(self,*args):
		self.internal_get()

	def transitional_post(self,*args):
		self.internal_post()

	def get(self,*args):
		self.auth_check()

		new_args = []
		for arg in args:
			new_args.append(str(arg))
		args = new_args
		self.transitional_get(args)
	
	def post(self,*args):
		self.auth_check()

		new_args = []
		for arg in args:
			new_args.append(str(arg))
		args = new_args

		self.transitional_post(args)

class LLHandler(LLDefaultHandler):
	
	def auth_check(self):
		self.session = get_current_session()
		
		return True
		



class LLGAEHandler(LLDefaultHandler):
	
		
	def auth_check(self):
		user = users.get_current_user()
		logging.debug("Current user is "+ str(user))
		if user:
			
			self.session = get_current_session()
			self.current_account = None
			self.set("current_user",user)
			if self.session.has_key("current_account"):
				self.current_account = self.session["current_account"]	
			else:
				self.current_account = STAccount.all().filter('email = ',user.email()).get()
				
				if not self.current_account:
					self.current_account = STAccount()
					self.current_account.email = user.email()
					#self.current_account.put()
				#Setting the session data
				self.current_account.last_entrance = datetime.datetime.now()
				self.current_account.put()
				if self.current_account.is_administrator:
					self.session["current_account"] = self.current_account
					#self.session["current_account"].put()
					time.sleep(1)
					return True
				else:
					self.session["current_account"] = self.current_account
					time.sleep(1)
					return True
					#self.redirect('/error/403')		
			
				
		else:
			self.redirect(users.create_login_url(self.request.uri))
        
			
	
