from django.db import models
from django.urls import reverse
from sorl.thumbnail import ImageField
from accounts.models import CustomUser
from django.contrib.auth import get_user_model


class Music(models.Model):
    RATING_CHOICES = (
        (1, 'poor'),
        (2, 'average'),
        (3, 'good'),
        (4, 'very good'),
        (5, 'excellent'),
    )

    title = models.CharField(max_length=50)
    Artist = models.ForeignKey('Artists', on_delete=models.CASCADE, null=True)
    language = models.CharField(choices=(
        ('iri', 'farsi'),
        ('eng', 'english'),),
        max_length=3, blank=True)
    audio = models.FileField(upload_to='audios/', blank=True)
    cover = ImageField(upload_to='covers/', blank=True)
    download_link = models.CharField(max_length=100)
    rating = models.IntegerField(choices=RATING_CHOICES, default=1)
    genres = models.CharField(choices=CustomUser.MUSIC_CATG_CHOICES, max_length=2, default=1)
    instrument_used = models.CharField(choices=CustomUser.MUSIC_instrument_CHOICES, max_length=2, blank=True)
    Album = models.ForeignKey('Album', on_delete=models.CASCADE, blank=True, null=True)
    view_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_view', args=[self.id])


class Favorits(models.Model):
    id = models.AutoField(primary_key=True)
    song = models.ForeignKey(Music, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), models.CASCADE)
    is_favorit = models.BooleanField(default=False)


class PlayList(models.Model):
    playlist_name = models.CharField(max_length=100)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.playlist_name


class PlaylistSongs(models.Model):
    playlist = models.ForeignKey(PlayList, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    song_name = models.CharField(max_length=100)
    audios = models.FileField(upload_to='playlist_audios/')


class Album(models.Model):
    Album_name = models.CharField(max_length=100)
    Artist = models.ForeignKey('Artists', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    genres = models.CharField(choices=CustomUser.MUSIC_CATG_CHOICES, max_length=2, blank=True)
    cover = ImageField(upload_to='album_covers/')

    def get_absolute_url(self):
        return reverse('album_songs', args=[self.id])

    def __str__(self):
        return self.Album_name


class AlbumSongs(models.Model):
    Album = models.ForeignKey(Album, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    song = models.ForeignKey(Music, on_delete=models.CASCADE)

class Artists(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class View(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    ip = models.CharField(max_length=20)
    song = models.ForeignKey(Music, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.song}:{self.ip}'
