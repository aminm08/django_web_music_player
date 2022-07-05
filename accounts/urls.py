from django.urls import path
from . import views
urlpatterns = [
    path('edit_profile/<int:pk>/',views.user_update_view,name='update_profile'),
]