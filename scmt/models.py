from django.db import models
from django import forms

"""
Event Attributes

StartDate - Presumably the date the event will start being shown on the STAR
EndDate - Presumably the date the event will stop being shown on the STAR
StartTime - Either an accompaniment to StartDate or standalone attribute that indicates the time of day the event will start
EndTime - Ditto but it indicates the time of day the event will end

Logo - This has something to do with DomesticAds and I can't remember what

SystemId - If the SystemId in the MPC is NOT this, the event does not show up
HeadendId - Ditto but with HeadendId
MsoCode - You get the deal, same but with MsoCode.
StateCode - State abbreviation. But other than that same deal.
DmaCode - DmaCode needs to match. You get the deal.
AreaServed - I presume any ZIP code in the MPC AreaServed field that matches will cause the event to show up.
"""

# Create your models here.
class Mso(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(help_text="For your reference.", blank=True)
    code = models.CharField(max_length=5, unique=True, help_text="The unique code for this MSO. Must match MsoCode in any MPCs for STARs from this MSO.")
    specialmessage = models.TextField(verbose_name="Special Message", help_text="The content of the SpecialMessage.xml entry for this MSO. Leave blank for none.", blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "MSO"

class Star(models.Model):
    class StarTypeChoices(models.TextChoices):
        HD = "HD", "IntelliSTAR 2 HD (waow good for you)"
        JR = "JR", "IntelliSTAR 2 Jr"
        XD = "XD", "IntelliSTAR 2 xD"
    friendlyName = models.CharField(verbose_name="Friendly Name", max_length=100)
    heId = models.CharField(verbose_name="Headend ID", max_length=7, unique=True, help_text="The unique ID for this STAR. Must match HeadendId in your MPC.")
    description = models.TextField()
    mso = models.ForeignKey(Mso, on_delete=models.CASCADE, verbose_name="MSO")
    starType = models.CharField(verbose_name="STAR Type", max_length=2, choices=StarTypeChoices.choices)    
    locale = models.CharField(max_length=50, help_text="Should match the place in HeadendName.")
    class Meta:
         verbose_name = "STAR"

    def __startype_to_prefix__(self):
        if self.starType == "HD":
            return "HD - "
        elif self.starType == "JR":
            return "ADOM - "
        elif self.starType == "XD":
            return "HD XD - "
        else:
            return "LMAO IDK - "
    
    def __startype_to_suffix__(self):
        if self.starType == "HD":
            return " - HD"
        elif self.starType == "JR":
            return " - ADOM"
        elif self.starType == "XD":
            return " - HD"
        else:
            return " - LMAO IDK"

    def __str__(self):
        # will look something like "the optiplex i2 (HD XD - N EVERETT-HQ - HD | 013011)"
        return f"{self.friendlyName} ({self.__startype_to_prefix__()}{self.locale}{self.__startype_to_suffix__()} | {self.heId})"

class AffiliateAd(models.Model):
    star = models.ForeignKey(Star, on_delete=models.CASCADE, related_name="affiliate_ads")
    crawl_content = models.TextField(help_text="The content of the crawl for this ad. This should be a valid XML fragment that can be directly inserted into the AffiliateAds.xml template.")
    friendlyName = models.CharField(max_length=100, help_text="A friendly name for this ad, for your reference.")

    def __str__(self):
        return f"{self.friendlyName} ({self.star.friendlyName})"
    class Meta:
        verbose_name = "Ad Crawl"

class Greeting(models.Model):
    star = models.ForeignKey(Star, on_delete=models.CASCADE, related_name="greetings")
    line1 = models.CharField(max_length=100, help_text="The first line of the greeting. This should be a short phrase that will be displayed on the STAR's screen.")
    line2 = models.CharField(max_length=100, blank=True, help_text="The second line of the greeting. This should be a short phrase that will be displayed on the STAR's screen.")

    def __str__(self):
        return f"{self.line1} {self.line2} ({self.star.friendlyName})"

    def linebreak(self):
        if self.line2 and self.line2.strip():
            return f"{self.line1}\\n{self.line2}"
        return self.line1