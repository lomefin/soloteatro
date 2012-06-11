import model.models
from model.properties import GenderProperty
from model.properties import SlugProperty
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
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

class STMontage(STModel):
	name = db.StringProperty()
	director = db.StringProperty()
	genre = db.StringProperty()
	slug = db.StringProperty()
	description = db.TextProperty()


class STSeason(STModel):
	
	start = db.DateTimeProperty()
	end = db.DateTimeProperty()
	prices = db.StringListProperty()
	venue = db.ReferenceProperty(STVenue,collection_name='seasons')
	montage = db.ReferenceProperty(STMontage,collection_name='seasons')
	

	repetition = db.IntegerProperty()

	#Technical Sheet
	writer = db.StringProperty()
	cast = db.StringListProperty()
	producer = db.StringProperty()
	technical_team = db.StringListProperty()


class STPlay(STModel):
	date = db.DateTimeProperty()
	season = db.ReferenceProperty(STSeason, collection_name='plays')

class STSeasonMedia(polymodel.PolyModel):
	season = db.ReferenceProperty(STSeason,collection_name='related_media')

class STSynopsis(STSeasonMedia):
	url = db.StringProperty()

class STInterview(STSeasonMedia):
	byline = db.StringProperty()
	content = db.TextProperty()

class STPicture(STSeasonMedia):
	url = db.StringProperty()

###Old stuff down there


# class LLCategory(LLModel):
# 	name = db.StringProperty()

# class LLPostedElement(polymodel.PolyModel):
# 	format = db.StringProperty()
# 	date_created = db.DateTimeProperty(auto_now_add=True) 
# 	is_active = db.BooleanProperty(default=True)
# 	creator = db.ReferenceProperty(LLAccount,collection_name='posts')
# 	date_published = db.DateTimeProperty
# 	title = db.StringProperty()
# 	possible_slug = db.StringProperty()
# 	slug = SlugProperty(possible_slug)
# 	short_url = db.StringProperty()
	
# class LLArticle(LLPostedElement):
# 	text = db.TextProperty()
# 	tags = db.StringListProperty()

# class LLNews(LLPostedElement):
# 	text = db.TextProperty()
# 	tags = db.StringListProperty()	


# class LLPlay(LLPostedElement):
# 	synopsis = db.TextProperty()
# 	tags = db.StringListProperty()
# 	category = db.ReferenceProperty(LLCategory,collection_name='plays')

# class LLPostReply(LLModel):
# 	replier_name = db.StringProperty()
# 	reply = db.StringProperty(multiline=True)
# 	element_replied = db.ReferenceProperty(LLPostedElement,collection_name='replies')


# class LLImage(LLModel):
# 	description = db.StringProperty()
# 	tags = db.StringListProperty()
# 	content = db.BlobProperty()
# 	content_type = db.StringProperty()
# 	image_size = db.StringProperty()
# 	parent_element = db.ReferenceProperty(LLPostedElement,collection_name='images')

