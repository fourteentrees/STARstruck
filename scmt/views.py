from django.shortcuts import render
from .models import Star, Mso, AffiliateAd, Greeting, WxDotComPromoText

def affiliateads_xml(request, star_id):
    star = Star.objects.get(heId=star_id)
    affiliate_ads = AffiliateAd.objects.filter(star=star)
    crawls = [{"attrs": w.get_attributes(),
         "content": w.crawl_content,        }
        for w in affiliate_ads
    ]
    main_attr = star.get_startrandom_crawl()
    return render(request, "AffiliateAds.xml", {"crawls": crawls, "star_id": star_id, "main_attr": main_attr}, content_type="application/xml")

def lot8_WpTp_xml(request, star_id):
    star = Star.objects.get(heId=star_id)
    greetings = Greeting.objects.filter(star=star)
    wptps = [
        {"attrs": w.get_attributes(),
         "wptps": w.linebreak(),
        }
        for w in greetings
    ]
    main_attr = star.get_startrandom_greeting()
    return render(request, "LOT8WelcomeProductTextPhrases.xml", {"wptps": wptps, "star_id": star_id, "main_attr": main_attr}, content_type="application/xml")


def promotext_xml(request, star_id):
    star = Star.objects.get(heId=star_id)
    promotexts = WxDotComPromoText.objects.filter(star=star)
    promotext = [
        {"attrs": w.get_attributes(),
         "promo": w.message,
        }
        for w in promotexts
    ]
    return render(request, "WxDotComPromoText.xml", {"promotexts": promotext, "star_id": star_id}, content_type="application/xml")

def specialmessage_xml(request):
    # get all Mso records and build a list of dicts with code + message
    msos = Mso.objects.filter(specialmessage__isnull=False).exclude(specialmessage__exact='')
    events = [
        {"code": m.code,
         "message": m.specialmessage
        }
        for m in msos
    ]
    return render(request, "SpecialMessage.xml", {"events": events}, content_type="application/xml")

def ping(request):
    # return just "ok"
    return render(request, "ping.txt", content_type="application/text")