from django.urls import path
from .import views
urlpatterns = [
    path('',views.main_page_view,name='main_page'),
    path('single_tracks/<int:pk>/',views.music_detail_view,name='detail_view'),
    path('playlists/',views.all_user_playlists,name='playlists'),
    path('delete_playlists/<int:pk>/',views.all_user_playlist_delete_view,name='playlist_delete'),
    path('playlists/<str:playlist_name>/',views.playlist_detail,name='playlist_songs'),
    path('favorits/',views.favorit_songs,name='favorit_songs'),
    path('search_answer/<str:word>/',views.search_view,name='search'),
    path('add_playlist/',views.play_list_add,name='add_playlist'),
    path('playlists/add_song/<int:pk>/',views.play_list_song_add,name='add_playlist_song'),
    path('all_songs/',views.all_songs,name='all_songs'),
    path('album/',views.album_list_view,name='albums'),
    path('album_songs/<int:pk>/',views.album_detail_view,name='album_songs'),
    # artists
    path('artists/', views.artist_view, name='artists'),
    path('artists/<str:artist>/', views.artist_songs_view, name='artist_songs'),
    # genres and instruments
    path('genres/<str:name>/',views.genres_view,name='genres'),
    path('instruments/<str:name>/',views.instrument_view,name='instruments'),
    # by language
    path('english/', views.english_songs, name='english'),
    path('farsi/', views.farsi_songs, name='farsi'),
    # other
    path('contactus/', views.contact_view, name='contact'),
    path('aboutus/', views.about_view, name='about'),
    path('profile/', views.profile_view, name='profile'),
]