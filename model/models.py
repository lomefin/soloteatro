import model.models
from model.properties import GenderProperty
from model.properties import SlugProperty
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.api import datastore_errors
from google.appengine.ext.webapp import template

from google.appengine.ext.db import polymodel

class STModel(db.Model):
	date_created = db.DateTimeProperty(auto_now_add=True) 
	is_active = db.BooleanProperty(default=True)
	
class STVenue(STModel):
	name = db.StringProperty()
	address = db.StringProperty()
	location = db.GeoPtProperty()
	telephone = db.StringProperty()
	parking = db.StringProperty()
	url = db.StringProperty()
	slug = SlugProperty(name)
	twitter = db.StringProperty()
	facebook = db.StringProperty()

class STMontage(STModel):
	name = db.StringProperty()
	director = db.StringProperty()
	company = db.StringProperty()
	genre = db.CategoryProperty()
	slug = db.StringProperty()
	description = db.TextProperty()
	writer = db.StringProperty()



class STSeason(STModel):
	
	start = db.DateTimeProperty()
	end = db.DateTimeProperty()
	prices = db.StringListProperty()
	venue = db.ReferenceProperty(STVenue,collection_name='seasons')
	montage = db.ReferenceProperty(STMontage,collection_name='seasons')
	
	status = db.CategoryProperty()
	repetition = db.IntegerProperty()
	genre = db.CategoryProperty()
	#Technical Sheet
	cast = db.StringListProperty()
	producer = db.StringProperty()
	technical_team = db.StringListProperty()



class STPresentation(STModel):
	date = db.DateTimeProperty()
	day  = db.DateTimeProperty()
	time = db.TimeProperty()
	season = db.ReferenceProperty(STSeason, collection_name='presentations')

class STSeasonMedia(polymodel.PolyModel):
	season = db.ReferenceProperty(STSeason,collection_name='related_media')
	montage = db.ReferenceProperty(STMontage,collection_name='related_media')
	parent_media = db.SelfReferenceProperty(collection_name='related_media')
	selected = db.BooleanProperty(default=False)
	description = db.StringProperty()

class STVideo(STSeasonMedia):
	video_id = db.StringProperty()
	provider = db.StringProperty()
	failsafe_url = db.StringProperty()

class STInterview(STSeasonMedia):
	byline = db.StringProperty()
	content = db.TextProperty()

class STPicture(STSeasonMedia):
	url = db.StringProperty()

class STImage(STSeasonMedia):
	fast_url = db.StringProperty()
	payload = blobstore.BlobReferenceProperty()

class STAccount(STModel):

	system_login = db.StringProperty()
	system_password = db.StringProperty()
	
	email = db.EmailProperty()
	wants_email = db.BooleanProperty()
	
	name = db.StringProperty()
	surname = db.StringProperty()
	maiden_name = db.StringProperty()
	
	last_entrance = db.DateTimeProperty()
	active = db.BooleanProperty()
	
	is_administrator	= db.BooleanProperty()