#!/usr/bin/env python
#
# Copyright 2012 Leonardo Luarte, 2007 Google Inc.
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

class DefaultHandler(STHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		
		calendar_start_date = datetime.date.today() - datetime.timedelta(days = datetime.date.today().isoweekday()-1)
		calendar_end_date = calendar_start_date + datetime.timedelta(weeks=4)
		calendar_end_date = calendar_end_date + datetime.timedelta(days = 7 - calendar_end_date.isoweekday())
		
		current_date = calendar_start_date
		month_weeks = []
		current_month = datetime.date.today().month
		while(current_date <= calendar_end_date):
			week = []
			for i in range(7):
				current_day = {'day':current_date.day,'current_month':current_month == current_date.month}
				current_date += datetime.timedelta(days=1)
				week.append(current_day)
			month_weeks.append(week)


		rand_seasons = db.GqlQuery("SELECT * FROM STSeason WHERE status = 'Open' LIMIT 3")
		self.set("rand_seasons",rand_seasons)
		self.set("calendar_weeks",month_weeks)
		self.render('index')

def main():
  LLApp([('/', DefaultHandler)])

if __name__ == "__main__":
  main()



