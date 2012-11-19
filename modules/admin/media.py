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
        video.parent_season = season.key()
        video.parent_montage = season.montage.key()

        video.video_id = self.param('youtube_id')
        provider = db.StringProperty('youtube')
        failsafe_url = db.StringProperty('http://www.youtube.com/embed/'+self.param('youtube_id'))

        video.put()

        self.set_flash('El video ha sido agregado a la temporada')
        self.redirect('/admin/montages/'+montage.slug)



class AddPictureToSeason(llhandler.LLGAEHandler):

    def base_directory(self):
        return os.path.dirname(__file__)
    
    def transitional_post(self, args):
        self.internal_post(args[0])   

    def save_picture_thumb(self, picture, thumb_url, thumb_name = "default"):
        picture_thumb = STThumb()
        picture_thumb.picture = picture
        picture_thumb.url = thumb_url
        picture_thumb.size = thumb_name
        picture_thumb.put()

    def get_thumb_from_picture(self,results,picture, thumb_type, original_id):
        if results.has_key(thumb_type):
                for thumb in results[thumb_type]:
                    if thumb['original_id'] == original_id:
                        self.save_picture_thumb(picture,thumb['url'], thumb_type)

    def internal_post(self, season_key):

        transloadit_response = json.loads(self.param("transloadit"))
        
        season_key = db.Key(encoded=season_key)
        season = STSeason.get(season_key)

        picture = STPicture()
        picture.season = season.key()
        picture.montage = season.montage.key()
        picture.parent_season = season.key()
        picture.parent_montage = season.montage.key()
        picture.put()
        
        uploads = transloadit_response['uploads']
        results = transloadit_response['results']

        for upload in uploads:
            original_id = upload['original_id']
            self.get_thumb_from_picture(results,picture,'thumb',original_id)
            self.get_thumb_from_picture(results,picture,'carrousel',original_id)

        self.set_flash('La image ha sido agregada a la temporada')
        self.redirect('/admin/montages/'+season.montage.slug)
        
