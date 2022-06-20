from django.contrib import admin
from .models import *


class AdminCostomize(admin.ModelAdmin):
    list_display = ['title', 'Artist', 'genres', 'instrument_used','pk']


admin.site.register(Music, AdminCostomize)
#----------------------------

class AdminFavCustomize(admin.ModelAdmin):
    list_display = ['song', 'user', 'is_favorit', 'id']


admin.site.register(Favorits, AdminFavCustomize)

#======================================


class AdminPlaylistCustomize(admin.ModelAdmin):
    list_display = ['playlist_name', 'user','datetime',]


admin.site.register(PlayList, AdminPlaylistCustomize)

#================================
class AdminPlaylistSongsCustomize(admin.ModelAdmin):
    list_display = ['playlist', 'user','song_name',]


admin.site.register(PlaylistSongs, AdminPlaylistSongsCustomize)


#=========================================
class AdminAlbumCustomize(admin.ModelAdmin):
    list_display = ['Album_name', 'Artist','user','datetime','genres']


admin.site.register(Album, AdminAlbumCustomize)

#============================
class AdminAlbumSongsCustomize(admin.ModelAdmin):
    list_display = ['Album','user','song',]


admin.site.register(AlbumSongs, AdminAlbumSongsCustomize)

#============================

class AdminAritstsCustomize(admin.ModelAdmin):
    list_display = ['name', 'date_of_birth', ]
    ordering = ['name', ]


admin.site.register(Artists, AdminAritstsCustomize)


# ============================
class AdminViewsCustomize(admin.ModelAdmin):
    list_display = ['ip', 'song', 'user']
    ordering = ['song', ]


admin.site.register(View, AdminViewsCustomize)
