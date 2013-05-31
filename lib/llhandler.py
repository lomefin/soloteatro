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



class LLDefaultHandler(webapp2.RequestHandler):
    def __init__(self,request,response):
        self.initialize(request, response)
        self.flash = None
        self.flash_type = 'success'
        self.log_count = 1
        self.values = {}
        self.logger = logging.getLogger(__name__)
        self.debug = True
        
        self.jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(root_dir.from_root_directory('views')))
        self.jinja_environment.filters['datetime'] = self.format_datetime      
        self.jinja_environment.filters['list'] = self.format_list
        #self.auth_check()


    month_names = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
    day_names   = ['lunes','martes','mi&eacute;rcoles','jueves','viernes','s&aacute;bado','domingo']

    def name_day(self,day):
        return LLDefaultHandler.day_names[int(day)]
    def name_month(self,month):
        return LLDefaultHandler.month_names[int(month)-1]

    def format_datetime(self, value, format='medium'):
        if format == 'SHORT_DATE_FORMAT':
            format = "%d de " + self.name_month(value.strftime("%m"))
        elif format == "MEDIUM_DATE_FORMAT":
            format = self.name_date(value.strftime("%w")) + " %d de " + self.name_month(value.strftime("%m"))
        elif format == 'SHORT_DATETIME_FORMAT':
            format = "%d de "+self.name_month(value.strftime("%m"))+", %H:%m hrs."
        elif format == 'JUST_TIME':
            format = "HH:mm hrs"
        elif format == 'full':
            format="EEEE, d. MMMM y 'at' HH:mm"
        elif format == 'medium':
            format="EE dd.MM.y HH:mm"
        return value.strftime(format)

    def format_list(self,list):
        if len(list) == 1:
            return list[0]
        if len(list) == 0:
            return ""
        try:
            return ", ".join(list[:-1])+" y "+list[-1]
        except:
            logging.debug("Error in format_list " + str(list))
            return ", ".join(list)

    def dispatch(self):
        config = {'secret_key': 'my-super-secret-key'}
        
        # Get a session store for this request.
        self.session_store = sessions.SessionStore(request=self.request,config=config)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)


    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session(name='soloteatro',factory=sessions_memcache.MemcacheSessionFactory)

    
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
        
        if template_values:
            self.values.update(template_values)
            
        try:
            self.read_flash()
            
            self.values['flash'] = self.flash
            self.values['flash_type'] = self.flash_type
            
            if self.current_account:
                self.values['logged_user'] = self.current_account
            if self.login_url:
                self.values['login_url'] = self.login_url
            if self.session.has_key("current_account"):
                self.values['logged_user'] = self.session["current_account"]
            if self.logout_url:
                self.values['logout_url'] = self.logout_url
            
        except:
            pass
        self.values.update({'current_url':self.request.url,'current_host':self.request.host_url})
        logging.debug("Want to render " + pagename)
        template = self.jinja_environment.get_template(pagename+'.html')
        
        # path = os.path.join(self.base_directory(), 'views/'+pagename+'.html')
        # template_file = open(path) 
        # compiled_template = template.Template(template_file.read()) 
        # template_file.close() 
        self.response.write(template.render(self.values)) 
        # self.response.write(compiled_template.render(template.Context(self.values)))
        
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
        return True
        #self.session = get_current_session()
        
        return True
        



class LLGAEHandler(LLDefaultHandler):
    
        
    def auth_check(self):
        user = users.get_current_user()
        logging.debug("Current user is "+ str(user))
        if user:
            
            self.current_account = None
            self.set("current_user",user)
            if self.session.has_key("current_account"):
                self.current_account = STAccount.get(db.Key(encoded=self.session["current_account"]))
            else:
                self.current_account = STAccount.all().filter('email = ',user.email()).get()
                
                if not self.current_account:
                    self.current_account = STAccount()
                    self.current_account.email = user.email()
                    #self.current_account.put()
                #Setting the session data
                self.current_account.last_entrance = datetime.datetime.now()
                self.current_account.put()

                self.session["current_account"] = str(self.current_account.key())
                time.sleep(1)
                return True
                
            
                
        else:
            self.redirect(users.create_login_url(self.request.uri))
        
            

