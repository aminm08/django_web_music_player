from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import *
class MusicPlayerTest(TestCase):
    def setup_date_for_other_tests(cls):
        cls.user = get_user_model().objects.create(username='testuser')
        cls.music = Music.objects.create(
            title = 'test_song',
            Artist = Artists.objects.all()[1],
            download_link = 'https://uupload.ir/view/halsey_without_me_128_l3kk.mp3/',
            rating = Music.RATING_CHOICES[0][0],
            genres = CustomUser.MUSIC_CATG_CHOICES[0][0],
            instrument_used = CustomUser.MUSIC_instrument_CHOICES[0][0],
            Album = Album.objects.all()[0],
        )
    #urls test
    def test_main_page_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
    def test_main_page_url_by_name(self):
        response = self.client.get(reverse('main_page'))
        self.assertEqual(response.status_code,200)


    def test_detail_page_url_by_name(self):
        response = self.client.get(reverse('detail_view',args=self.music.pk))
        self.assertEqual(response.status_code,200)
