from django.contrib import admin

# Register your models here.
from .models import Mso, Star, AffiliateAd, Greeting
admin.site.register(Mso)
admin.site.register(Star)
admin.site.register(AffiliateAd)
admin.site.register(Greeting)
