# coding=utf-8
import model.models
import datetime
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

class STGenre(STModel):
	name = db.StringProperty()
	slug = db.StringProperty()
	rating = db.RatingProperty()
	
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
	genre = db.ReferenceProperty(STGenre, collection_name="montages")
	slug = db.StringProperty()
	description = db.TextProperty()
	writer = db.StringProperty()

	def delete(self):
		db.delete(self.seasons)

class STSeason(STModel):
	
	start = db.DateTimeProperty()
	end = db.DateTimeProperty()
	prices = db.StringListProperty()
	venue = db.ReferenceProperty(STVenue,collection_name='seasons')
	montage = db.ReferenceProperty(STMontage,collection_name='seasons')
	
	status = db.CategoryProperty()
	repetition = db.IntegerProperty()
	genre = db.ReferenceProperty(STGenre, collection_name="seasons")
	#Technical Sheet
	cast = db.StringListProperty()
	producer = db.StringProperty()
	technical_team = db.StringListProperty()

	last_shown = db.DateTimeProperty()

	@property
	def best_picture(self):
		return self.related_media.filter('class = ','STPicture').order('-priority').get().thumb_url

	@property
	def best_carrousel_picture(self):
		return self.related_media.filter('class = ','STPicture').order('-priority').get().carrousel_url		


class STPresentation(STModel):
	date = db.DateTimeProperty()
	day  = db.DateTimeProperty()
	time = db.TimeProperty()
	season = db.ReferenceProperty(STSeason, collection_name='presentations')

	def time_for_next_presentation(self):
		time_for_next_presentation = self.date - datetime.datetime.now()
		days = time_for_next_presentation.days
		hours = time_for_next_presentation.seconds/(3600*24)
		minutes = (time_for_next_presentation.seconds - (3600*24) * hours)/3600

		output = ""
		if days > 0:
			output = str(days) + " d&iacute;as "
			if days < 2:
				output = output + str(hours) + " horas "
				if hours > 0:
					output = output + str(minutes) + " minutos"
		if days == 0:
			if hours > 0:
				output = str(hours) + " horas "
			if minutes > 1:
				output = output + str(minutes) + " minutes"
		return output

class STSeasonMedia(polymodel.PolyModel):
	season = db.ReferenceProperty(STSeason,collection_name='related_media')
	montage = db.ReferenceProperty(STMontage,collection_name='related_media')
	parent_media = db.SelfReferenceProperty(collection_name='related_media')
	selected = db.BooleanProperty(default=False)
	description = db.StringProperty()
	visible = db.BooleanProperty(default=True)
	priority = db.IntegerProperty(default=1)

class STVideo(STSeasonMedia):
	video_id = db.StringProperty()
	provider = db.StringProperty()
	failsafe_url = db.StringProperty()
	
class STArticle(STModel):
	title = db.StringProperty()
	body = db.TextProperty()
	slug = SlugProperty(title)

class STInterview(STSeasonMedia):
	byline = db.StringProperty()
	content = db.TextProperty()
	visible = False


class STPicture(STSeasonMedia):
	@property
	def url(self):
		return self.thumbs.filter('size = ','carrousel').get().url
	@property
	def carrousel_url(self):
		return self.thumbs.filter('size = ','carrousel').get().url
	@property
	def thumb_url(self):
		return self.thumbs.filter('size = ','thumb').get().url

class STThumb(STModel):
	picture = db.ReferenceProperty(STPicture,collection_name='thumbs')
	url = db.StringProperty()
	size = db.StringProperty()

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