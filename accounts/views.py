from django.shortcuts import render
from django.views import generic
from .forms import CustomUserCreationForm,CustomUserChangeForm
from django.urls import  reverse_lazy
from .models import CustomUser
from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required



def sign_up_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = CustomUserCreationForm()
    return render(request,'registration/signup.html',{'form':form})

@login_required()
def user_update_view(request,pk):
    user  = get_object_or_404(CustomUser,pk=pk)
    form = CustomUserChangeForm(request.POST or None,instance=user)
    if user.username == str(request.user):

        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'registration/update_profile.html', {'form': form})
    else:
        return render(request,'404.html')
