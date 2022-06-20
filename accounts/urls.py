from django.urls import path
from . import views
urlpatterns = [
    path('signup/',views.sign_up_view,name='signup'),
    path('edit_profile/<int:pk>/',views.user_update_view,name='update_profile'),
]