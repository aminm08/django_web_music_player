from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator
from accounts.models import CustomUser
from ipware import get_client_ip
from random import randint
from .decorators import user_passes_test,check_user_and_adder

import os

from .forms import *
from .models import *




def main_page_view(request):
    #vars
    word = ''
    random_suggestion = []
    all_musics = Music.objects.all() # all songs
    random_musics = pick_random(all_musics,5) # geting random songs pick_random is a function wich has been  defined in the bottom
    up_rates = Music.objects.filter(rating=5)

    if request.user.is_authenticated:  # if user is authenticated we will show some suggestions by his favorites wich had choosed in the authenticatipn
        user = CustomUser.objects.get(username=request.user) # finding the user
        sugg = Music.objects.filter(instrument_used=user.favorite_instrument,genres=user.favorite_musics)
        random_suggestion = pick_random(sugg,5) # pick 5 song from suggestion there might be less than 5 , so we will show 5 or less
        # if user search something
    if request.method == 'POST':
        word = request.POST.get('search')
        return redirect('search', word=word)

    return render(request, 'musics/musics_list_view_temp.html',
                  context={'random': random_musics,
                           'up_rates': up_rates,
                           'random_sugg': random_suggestion})
#-=====================================================================
def pick_random(musics,num):
    random_musics = []
    if len(musics) >num:
        while len(random_musics)!=num: # getting random songs ,you can change the number (3) based on number of songs you have in site

            number = randint(0,len(musics)-1)  # i started from 0 because our songs are in a list and it starts from 0 and len(all)-1 for the same reason
            if musics[number] not in random_musics:
                random_musics.append(musics[number])
        return random_musics
    else:
        return musics
#=======================================================

def music_detail_view(request, pk):  # any user can access detail view
    random_sugg = []
    # it gets the user ip adr
    ip = get_client_ip(request)[0]
    # getting music by the pk
    music = get_object_or_404(Music, pk=pk)
    all = Music.objects.all()
    #==================VIEWS MANAGMENT==========
    if len(View.objects.all())!=0 : # to prevent eror when there's no object of this model(no view for the song)
        all_user_views = View.objects.filter(Q(user=request.user)|Q(ip=ip),song=music)# cheking if this user has any views of this song
        if len(all_user_views) == 0:# if this user has no view for this song we can add the view wich means th user is uniqe
            View.objects.create(user=request.user,ip=ip,song=music)
    else:
        View.objects.create(user=request.user, ip=ip, song=music)
    music_views = View.objects.filter(song=music) # getting views for the music

    #=============SUGGESTION MANAGMENT==================

    if request.user.is_authenticated:
        sugg = [i for i in Music.objects.filter(Q(Artist=music.Artist)|Q(genres=music.genres)) if i.title != music.title]#getting the user's suggestions
        if len(sugg) <3 and len(sugg) != 0:
            random_sugg = pick_random(all,3) # we will pick from all if the music suggs are less than 3

        if len(sugg) >=3:
            random_sugg = pick_random(sugg,3)#chosing random songs from sugg



    if request.method == 'POST' and request.user.is_authenticated:  # to add the song to favorits only for authenticated users
        form = FavForm(request.POST)
        if form.is_valid():
            if check_fav_list(request, music):  # checks if the song is already in the favorites list
                is_fav = form.save(commit=False)
                is_fav.user = request.user
                is_fav.song = music
                is_fav.save()
    else:
        form = FavForm()

    return render(request, 'musics/musics_detail_view_temp.html',
                  {'music': music, 'form': form, 'isin': check_fav_list(request, music),'sugg':random_sugg,'views':len(music_views)})
#======================================================================================

# checks if the music is in favorite list or not
def check_fav_list(request, music):
    # return true for anonymous user we prevented showing the form to anonymoususer in template
    if not request.user.is_authenticated:
        return True
    # getting favorite songs of this user
    songs = Favorits.objects.filter(user=request.user)
    # ckeks if that favorite list has any song or not
    if len(songs) != 0:
        for i in songs:
            if str(i.song) == music.title and i.user == request.user and i.is_favorit == True:
                # it means the song is in favorits so we send false to make the if statement in detail view  false
                return False
        # else for {for} it means that there is no song with these infos in favorite list
        else:
            return True
    # returns true if there's no song in favorite list
    else:
        return True

#====================================================
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
@user_passes_test(check_user_and_adder,raise_exception=True,url_input_obj_name='pk')
def play_list_song_add(request, pk):
    playlist = get_object_or_404(PlayList, pk=pk)
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

#==========================================
@login_required()
def profile_view(request):

    return render(request, 'profile_temp.html')
    # instrumental orginize
#=======================================

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
        if word == '':
            print('enter somthing')
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
        if word == '':
            print('enter somthing')
        return redirect('search', word=word)

    return render(request,'musics/song_and_instrument.html',{'page_obj':page_obj,'catg':name})
#+=======================================


# by language


def english_songs(request):
    musics = Music.objects.filter(language='eng').order_by('-rating','-view_number')

    return render(request, 'musics/song_and_instrument.html', {'music': musics, 'catg': 'english'})
#==================================================

def farsi_songs(request):
    musics = Music.objects.filter(language='iri').order_by('-rating','-view_number')

    return render(request, 'musics/song_and_instrument.html', {'music': musics, 'catg': 'farsi'})
#==================================================


#artist
def artist_songs_view(request,artist):
    Artist = get_object_or_404(Artists,name=artist)
    songs = Music.objects.filter(Artist=Artist)

    return render(request, 'musics/artist_songs.html', {'artist':Artist, 'songs':songs})



#==================================================

def contact_view(request):

    return render(request,'contactus_page.html')

#==================================================
def about_view(request):

    return render(request,'aboutus_page.html')

