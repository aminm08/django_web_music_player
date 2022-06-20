from django.forms import ModelForm

from .models import *


class FavForm(ModelForm):
    class Meta:
        model = Favorits
        fields = ['is_favorit', ]


class PlaylistForm(ModelForm):
    class Meta:
        model = PlayList
        fields = ['playlist_name']


class PlaylistSongsForm(ModelForm):
    class Meta:
        model=PlaylistSongs
        fields=['song_name','audios']
