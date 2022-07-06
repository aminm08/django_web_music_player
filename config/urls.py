
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('allauth.urls')),
    path('accounts/',include('accounts.urls')),
    path('',include('musics.urls')),
    path('',include('pages.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# handler404 = "musics.views.eror_404"
