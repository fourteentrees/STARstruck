"""
URL configuration for starstruck project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from scmt import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/star/<star_id>/AffiliateAds.xml", views.affiliateads_xml, name="affiliateads_xml"),
    path("api/star/<star_id>/LOT8WelcomeProductTextPhrases.xml", views.lot8_WpTp_xml, name="lot8_wptp_xml"),
    path("api/SpecialMessage.xml", views.specialmessage_xml, name="specialmessage_xml"),
    path("api/ping", views.ping, name="ping"),
    path("api/star/<star_id>/WxDotComPromoText.xml", views.promotext_xml, name="promotext_xml"),
]

admin.site.site_header = 'STARstruck administration'
admin.site.site_title = 'STARstruck admin'
