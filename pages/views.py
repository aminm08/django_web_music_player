
from django.views.generic import TemplateView
class ContactView(TemplateView):
    template_name = 'contactus_page.html'
#==================================================
class AboutUsView(TemplateView):
    template_name = 'aboutus_page.html'
#============================
class ProfileView(TemplateView):
    template_name = 'profile_temp.html'
# =======================================

