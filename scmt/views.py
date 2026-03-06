from django.shortcuts import render
from .models import Star, Mso, AffiliateAd, Greeting, SpecialMessage

def affiliateads_xml(request, star_id):
    star = Star.objects.get(id=star_id)
    affiliate_ads = AffiliateAd.objects.filter(star=star)
    crawls = []
    for ad in affiliate_ads:
        crawls.append(ad)
    return render(request, "AffiliateAds.xml", {"crawls": crawls, "star_id": star_id}, content_type="application/xml")

def lot8_WpTp_xml(request, star_id):
    star = Star.objects.get(heId=star_id)
    greetings = Greeting.objects.filter(star=star)
    wptps = []
    for greeting in greetings:
        wptps.append(greeting)
    return render(request, "LOT8WelcomeProductTextPhrases.xml", {"wptps": wptpsa, "star_id": star_id}, content_type="application/xml")