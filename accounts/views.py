from django.shortcuts import render
from .forms import CustomUserChangeForm
from .models import CustomUser
from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

@login_required()
def user_update_view(request,pk):
    user  = get_object_or_404(CustomUser,pk=pk)
    form = CustomUserChangeForm(request.POST or None,instance=user)
    if user.username == str(request.user):

        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'account/update_profile.html', {'form': form})
    else:
        return render(request,'404.html')
