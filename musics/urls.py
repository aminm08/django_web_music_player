from django.urls import path
from .import views
urlpatterns = [
    #musics
    path('',views.main_page_view,name='main_page'),
    path('music/<int:pk>/',views.music_detail_view,name='detail_view'),
    path('music/add_music/',views.music_add_view,name='add_music'),
    #playlist
    path('playlists/',views.all_user_playlists,name='playlists'),
    path('playlists/delete/<int:pk>/',views.all_user_playlist_delete_view,name='playlist_delete'),
    path('playlists/<str:playlist_name>/',views.playlist_detail,name='playlist_songs'),
    path('playlists/add/', views.play_list_add, name='add_playlist'),
    path('playlists/song_add/<str:playlist_name>/', views.play_list_song_add, name='add_playlist_song'),
    #favorits
    path('favorits/',views.favorit_songs,name='favorit_songs'),
    #search
    path('search_answer/<str:word>/',views.search_view,name='search'),
    #all songs
    path('all_songs/',views.all_songs,name='all_songs'),
    #album
    path('albums/',views.album_list_view,name='albums'),
    path('albums/<int:pk>/',views.album_detail_view,name='album_songs'),
    path('albums/add/',views.album_add_view,name='add_album'),
    # artists
    path('artists/', views.artist_view, name='artists'),
    path('artists/<str:artist>/', views.artist_songs_view, name='artist_songs'),
    path('add_artist/',views.artist_add_view,name='add_artist'),
    # genres and instruments
    path('genres/<str:name>/',views.genres_view,name='genres'),
    path('instruments/<str:name>/',views.instrument_view,name='instruments'),
    # by language
    path('music/english/', views.english_songs, name='english'),
    path('music/farsi/', views.farsi_songs, name='farsi'),

]