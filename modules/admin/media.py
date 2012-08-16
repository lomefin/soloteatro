from lib.imports import *

class AddMediaToSeason(llhandler.LLGAEHandler):
    def base_directory(self):
        return os.path.dirname(__file__)
    
    def transitional_get(self, args):

        self.internal_get(args[0],args[1])

    def internal_get(self,montage_slug,season_numeral):

        montage = self.get_or_404(STMontage.all().filter('slug =',montage_slug).get())
        self.set('montage',montage)
        season = montage.seasons.filter('repetition =',season_numeral)
        self.set('season',season)
        self.render('add_media')



class AddMediaToLatestSeason(llhandler.LLGAEHandler):
    def base_directory(self):
        return os.path.dirname(__file__)
    
    def transitional_get(self, args):

        self.internal_get(args[0])

    def internal_get(self,montage_slug):

        montage = self.get_or_404(STMontage.all().filter('slug =',montage_slug).get())
        self.set('montage',montage)
        season = montage.seasons.order('-repetition').get()
        self.set('image_upload_url',blobstore.create_upload_url('/admin/media/image/'+str(season.key())))
        self.set('season',season)
        self.render('add_media')



class AddVideoToSeason(llhandler.LLGAEHandler):

    def base_directory(self):
        return os.path.dirname(__file__)
    
    def transitional_post(self, args):

        self.internal_post(args[0])

    def internal_post(self, season_key):

        season_key = db.Key(encoded=season_key)
        season = STSeason.get(season_key)
        logging.debug(season_key)
        montage = season.montage
        

        video = STVideo()
        video.season = season.key()
        video.montage = montage.key()

        video.video_id = self.param('youtube_id')
        provider = db.StringProperty('youtube')
        failsafe_url = db.StringProperty('http://www.youtube.com/embed/'+self.param('youtube_id'))

        video.put()

        self.set_flash('El video ha sido agregado a la temporada')
        self.redirect('/admin/montages/'+montage.slug)

class AddImageToSeason(blobstore_handlers.BlobstoreUploadHandler):
    def post(self,season_key):
        #try:
        season_key = db.Key(encoded=season_key)
        season = STSeason.get(season_key)
        logging.debug(season_key)
        montage = season.montage
        

        image = STImage()
        
        logging.debug(self.get_uploads())
        upload = self.get_uploads()[0]
        image.payload = upload.key()
        logging.warn("Got upload")
        logging.warn(image.payload)
        image.put()
        image.fast_url = images.get_serving_url(image.payload)
        picture = STPicture()
        picture.season = season.key()
        picture.montage = montage.key()
        picture.url = images.get_serving_url(image.payload)
        picture.put()

        #self.set_flash('La imagen ha sido agregado a la temporada')
        self.redirect('/admin/montages/'+montage.slug)

        #except :
        #    self.redirect('/upload_failure.html')

class AddImageToSeason2(llhandler.LLGAEHandler):

    def base_directory(self):
        return os.path.dirname(__file__)
    
    def transitional_post(self, args):

        self.internal_post(args[0])

    def internal_post(self, season_key):

        season_key = db.Key(encoded=season_key)
        season = STSeason.get(season_key)
        logging.debug(season_key)
        montage = season.montage
        

        image = STImage()
        image.season = season.key()
        image.montage = montage.key()

        image.payload = db.Blob(self.param('image_file'))
        
    
        image.put()
        image.fast_url = images.get_serving_url(image.payload.key())
        image.put()

        self.set_flash('La imagen ha sido agregado a la temporada')
        self.redirect('/admin/montages/'+montage.slug)


        
