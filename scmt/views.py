from django.shortcuts import render
from .models import Star, Mso, AffiliateAd, Greeting

def affiliateads_xml(request, star_id):
    star = Star.objects.get(heId=star_id)
    affiliate_ads = AffiliateAd.objects.filter(star=star)
    crawls = []
    for ad in affiliate_ads:
        crawls.append(ad.crawl_content)
    return render(request, "AffiliateAds.xml", {"crawls": crawls, "star_id": star_id}, content_type="application/xml")

def lot8_WpTp_xml(request, star_id):
    star = Star.objects.get(heId=star_id)
    greetings = Greeting.objects.filter(star=star)
    wptps = []
    for greeting in greetings:
        wptps.append(greeting.linebreak)
    return render(request, "LOT8WelcomeProductTextPhrases.xml", {"wptps": wptps, "star_id": star_id}, content_type="application/xml")

def specialmessage_xml(request):
    # get all Mso records and build a list of dicts with code + message
    msos = Mso.objects.filter(specialmessage__isnull=False).exclude(specialmessage__exact='')
    events = [{"code": m.code, "message": m.specialmessage} for m in msos]
    return render(request, "SpecialMessage.xml", {"events": events}, content_type="application/xml")

def ping(request):
    # return just "ok"
    return render(request, "ping.txt", content_type="application/text")