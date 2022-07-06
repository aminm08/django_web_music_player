from django.forms import ModelForm

from .models import *


class MusicForm(ModelForm):
    class Meta:
        model = Music
        fields = ['title', 'Artist', 'language', 'audio', 'cover',
                  'download_link', 'rating', 'genres', 'instrument_used', 'Album', ]

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


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['Album_name', 'Artist', 'genres', 'cover', ]


class ArtistForm(ModelForm):
    class Meta:
        model = Artists
        fields = ['name','date_of_birth']