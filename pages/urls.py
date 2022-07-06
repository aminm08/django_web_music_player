from django.urls import path

from . import views

urlpatterns = [
    path('contact_us/', views.ContactView.as_view(), name='contact'),
    path('about_us/', views.AboutUsView.as_view(), name='about'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]