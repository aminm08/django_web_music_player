from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Permission,Group
from django.contrib.contenttypes.models import ContentType

from random import randint





#this file contains function that used in our views and are not views
# (tools which used in our views in views.py)
#this file created for better management to views and other functions



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



# picks (num) random object from musics
def pick_random(musics,num):
    random_musics = []
    if len(musics) >num:
        # getting random songs ,you can change the number (3) based on number of songs you have in site
        while len(random_musics)!=num:
            # i started from 0 because list indexes are from 0 and len(all)-1 for the same reason
            number = randint(0,len(musics)-1)
            if musics[number] not in random_musics:
                random_musics.append(musics[number])
        return random_musics
    else:
        return musics
#=======================================================
# the test func for the userpassestest decorator
def check_user_and_adder(user,model_object,url_info): # url_info_containts the kwargs
    url_object_name = list(url_info.keys())[0] #there's a dict and we get the key with this method
    url_object_value = url_info.get(url_object_name) # getting the value by key
    # get the object depended on url variable name
    if url_object_name == 'pk':
        obj = get_object_or_404(model_object,pk=url_object_value)
    elif url_object_name == 'playlist_name':
        obj = get_object_or_404(model_object,playlist_name=url_object_value)
    return user == obj.user # true if this user is the same user in DB


def add_user_to_group():
    staffs_group, created = Group.objects.get_or_create(name='staff')
    # content_type = ContentType.objects.get_for_model(Music)
    all_users = get_user_model().objects.all()
    for user in all_users:
        if user.is_staff:
            user.groups.add(staffs_group)
