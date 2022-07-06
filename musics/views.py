from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator
from ipware import get_client_ip
from django.contrib.auth import get_user_model


import os

from .forms import *
from .models import *
from .decorators import user_passes_test
from .toolfuncs import pick_random,check_user_and_adder,check_fav_list,add_user_to_group



def main_page_view(request):
    #vars
    word = ''
    random_suggestion = []
    all_musics = Music.objects.all() # all songs
    add_user_to_group()
    # geting random songs pick_random is a function wich has been  defined in the bottom
    random_musics = pick_random(all_musics,5)
    up_rates = Music.objects.filter(rating=5)
    # if user is authenticated we will show some suggestions by its favorites which had chosen in the authentication
    if request.user.is_authenticated:
        user = get_user_model().objects.get(username=request.user) # finding the user
        suggestions = Music.objects.filter(instrument_used=user.favorite_instrument,genres=user.favorite_musics)
        # pick 5 song from suggestion there might be less than 5 , so we will show 5 or less
        random_suggestion = pick_random(suggestions,5)
    # if user search something
    if request.method == 'POST':
        word = request.POST.get('search')
        return redirect('search', word=word)

    return render(request, 'musics/musics_list_view_temp.html',
                  context={'random': random_musics,
                           'up_rates': up_rates,
                           'random_sugg': random_suggestion})
#-=====================================================================
def music_detail_view(request, pk):  # any user can access detail view
    random_sugg = []
    # it gets the user ip adr
    ip = get_client_ip(request)[0]
    # getting music by the pk
    music = get_object_or_404(Music, pk=pk)
    all = Music.objects.all()
    #==================VIEWS MANAGMENT==========
    # to prevent eror when there's no object of this model(no view for the song)
    if len(View.objects.all())!=0 :
        # cheking if this user has any views of this song
        all_user_views = View.objects.filter(Q(user=request.user)|Q(ip=ip),song=music)
        # if this user has no view for this song we can add the view wich means th user is uniqe
        if len(all_user_views) == 0:
            View.objects.create(user=request.user,ip=ip,song=music)
    else:# we add the view if views are 0
        View.objects.create(user=request.user, ip=ip, song=music)
    # getting views for the music
    music_views = View.objects.filter(song=music)

    #=============SUGGESTION MANAGMENT==================
    # suggest some songs that are not duplicated from songs when user is authenticated
    if request.user.is_authenticated:
        suggestions = [i for i in Music.objects.filter(Q(Artist=music.Artist)|Q(genres=music.genres)) if i.title != music.title]#getting the user's suggestions
        if len(suggestions) <3 and len(suggestions) != 0:
            # we will pick from all if the music suggs are less than 3
            random_suggestions = pick_random(all,3)
        # chosing random songs from suggesstions
        if len(suggestions) >=3:
            random_suggestions = pick_random(suggestions,3)

    # to add the song to favorits only for authenticated users
    if request.method == 'POST' and request.user.is_authenticated:
        form = FavForm(request.POST)
        if form.is_valid():
            # checks if the song is already in the favorites list
            if check_fav_list(request, music):
                is_fav = form.save(commit=False)
                is_fav.user = request.user
                is_fav.song = music
                is_fav.save()
    else:
        form = FavForm()

    return render(request, 'musics/musics_detail_view_temp.html',
                  {'music': music,
                   'form': form,
                   'isin': check_fav_list(request, music),
                   'sugg':random_sugg,'views':len(music_views)
                   })
#=======================================
@login_required()
@permission_required('can_add_music',raise_exception=True)
def music_add_view(request):
    if request.method == 'POST':
        form = MusicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_songs')
    else:
        form = MusicForm()
    return render(request,'musics/add_music_page.html',{'form':form})

#======================================
@login_required()
def favorit_songs(request):
    songs = Music.objects.filter(favorits__user=request.user, favorits__is_favorit=True).distinct()
    # the delete option
    if request.method == "POST":
        # getting song_id witch has sent as the name
        # @login_required() of our delete button[csrf_token,song_id]
        song_id = list(request.POST.keys())[1]
        # getting the song with pk , i checked the user and is_favorite for sure
        favorite_song = Favorits.objects.filter(user=request.user, song__id=song_id,is_favorit=True)
        favorite_song.delete()

    return render(request, 'musics/favs.html', {'fav_song': songs})

#======================================
def all_user_playlists(request):
    # getting all playlists of this user
    playlists = PlayList.objects.filter(user=request.user)
    if request.method == "POST":
        # getting playlist id which has sent as the name of button in html file
        playlist_id = list(request.POST.keys())[1]
        return redirect('playlist_delete',playlist_id)
    return render(request, 'musics/playlist_page.html', {'playlist': playlists})

#==========================================
@user_passes_test(check_user_and_adder,model_obj=PlayList,raise_exception=True,url_input_obj_name='pk')
#delete the playlist object by pk
def all_user_playlist_delete_view(request,pk):
    playlist = get_object_or_404(PlayList,pk=pk)
    if request.method =='POST':
        playlist.delete()
        return redirect('playlists')
    return render(request,'musics/playlist_delete_temp.html',{'playlist':playlist})
#=============================================

@user_passes_test(check_user_and_adder,model_obj=PlayList,raise_exception=True,url_input_obj_name='playlist_name')
@login_required()
def playlist_detail(request, playlist_name):
    songs = PlaylistSongs.objects.filter(playlist__playlist_name=playlist_name,playlist__user=request.user)  # playlist is a FK to playlist table
    playlist = get_object_or_404(PlayList,playlist_name=playlist_name)  # getting the playlist for adding music at later
    # delete the playlist
    if request.method == "POST":
        # getting song id which has sent as the name of the delete button
        playlist_id = list(request.POST.keys())[1]
        song = PlaylistSongs.objects.filter(pk=playlist_id,user=request.user)
        # getting the name of the song path to delete
        song_path = song[0].audios.name
        song.delete()  # deleting the song object
        os.remove(os.path.join(settings.MEDIA_ROOT, song_path))  # deleting the song file in the path wich had defined in setting

    return render(request, 'musics/playlist_songs_page.html',
                  {'songs': songs, 'pl_name': playlist_name, 'playlist': playlist})

#=-=============================================================

@login_required()
def play_list_add(request):
    if request.method == "POST":
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            playlist.save()
            return redirect('playlists')
    else:
        form = PlaylistForm()
    return render(request, 'musics/add_playlist_temp.html', {'form': form})
#=================================================================
@login_required()
@user_passes_test(check_user_and_adder,raise_exception=True,url_input_obj_name='playlist_name',model_obj=PlayList)
def play_list_song_add(request, playlist_name):
    playlist = get_object_or_404(PlayList, playlist_name=playlist_name)
    if request.method == "POST":
        form = PlaylistSongsForm(request.POST)
        if form.is_valid():
            song = form.save(commit=False)
            song.user = request.user
            song.playlist = playlist
            song.save()
            return redirect('add_playlist_song')
    else:
        form = PlaylistSongsForm()
    return render(request, 'musics/add_playlist_songs_temp.html', {'form': form, 'playlist': playlist})

#======================================================

def search_view(request, word):
    object_list = []
    # if user search somthing in the search page
    if request.method == 'POST':
        word = request.POST.get('search')
        object_list = Music.objects.filter(
            Q(title__icontains=word.strip().lower()) | Q(Artist__name__icontains=word.strip().lower()) | Q(
                genres__icontains=word.strip().lower()))
    # for the response to search from other pages
    if request.method == 'GET':
        object_list = Music.objects.filter(
            Q(title__icontains=word.strip().lower()) | Q(Artist__name__icontains=word.strip().lower()) | Q(
                genres__icontains=word.strip().lower()))
    return render(request, 'musics/search_answer.html', {'song': object_list, 'word': word})
#======================================================

def all_songs(request):
    musics = Music.objects.all()
    # paginator configuration
    paginator = Paginator(musics, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'musics/song_and_instrument.html', {'page_obj': page_obj, 'catg': 'all songs'})

#==================================================
def album_list_view(request):
    albums = Album.objects.all().order_by('-datetime')  # newest albums
    # paginator configguration
    paginator = Paginator(albums,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # if user search something
    if request.method == 'POST':
        word = request.POST.get('search')
        if word == '':
            print('enter somthing')
        return redirect('search', word=word)

    return render(request, 'musics/album_list_view_temp.html', {'page_obj':page_obj})
 #===============================================================

def album_detail_view(request, pk):
    album = get_object_or_404(Album, pk=pk)
    songs = AlbumSongs.objects.filter(Album=album)
    return render(request, 'musics/album_detail_view_temp.html', {'album': album, 'songs': songs})
#==========================================
@login_required()
@permission_required('can_add_album',raise_exception=True)
def album_add_view(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('albums')
    else:
        form = AlbumForm()
    return render(request,'musics/add_music_page.html',{'form':form})
#=========================================
def artist_view(request):
    artists = Artists.objects.all()
    # if user search something
    if request.method == 'POST':
        word = request.POST.get('search')
        if word == '':
            print('enter somthing')
        return redirect('search', word=word)
    return render(request, 'musics/artist_page.html', {'artists':artists})
#========================
@login_required()
@permission_required('can_add_artist',raise_exception=True)
def artist_add_view(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('artists')
    else:
        form = ArtistForm()
    return render(request,'musics/add_artist_page.html',{'form':form})

#==========================================
# categories views
def genres_view(request,name):

    musics = Music.objects.filter(genres=name[:2])
    #paginator configuration
    paginator = Paginator(musics, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # if user search something
    if request.method == 'POST':
        word = request.POST.get('search')
        return redirect('search', word=word)

    return render(request,'musics/song_and_instrument.html',{'page_obj':page_obj,'catg':name})
#========================================
def instrument_view(request,name):
    musics = Music.objects.filter(instrument_used=name[:2])# getting all things using name
    #paginator configuration
    paginator = Paginator(musics, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # if user search something
    if request.method == 'POST':
        word = request.POST.get('search')
        return redirect('search', word=word)

    return render(request,'musics/song_and_instrument.html',{'page_obj':page_obj,'catg':name})
# by language
#+=======================================
def english_songs(request):
    musics = Music.objects.filter(language='eng').order_by('-rating','-view_number')

    return render(request, 'musics/song_and_instrument.html', {'music': musics, 'catg': 'english'})
#==================================================

def farsi_songs(request):
    musics = Music.objects.filter(language='iri').order_by('-rating','-view_number')

    return render(request, 'musics/song_and_instrument.html', {'music': musics, 'catg': 'farsi'})
#==================================================

#artist songs
def artist_songs_view(request,artist):
    Artist = get_object_or_404(Artists,name=artist)
    songs = Music.objects.filter(Artist=Artist)

    return render(request, 'musics/artist_songs.html', {'artist':Artist, 'songs':songs})
#==================================================

