from django.db import models
from django import forms

"""
Event Attributes

StartDate - Presumably the date the event will start being shown on the STAR
EndDate - Presumably the date the event will stop being shown on the STAR
StartTime - Either an accompaniment to StartDate or standalone attribute that indicates the time of day the event will start
EndTime - Ditto but it indicates the time of day the event will end

Logo - This is used for backgrounds. When cueing a presentation the STAR will look for this in the backgrounds file and will set the bg to the corresponding image. Not much use here...

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
    specialmessage = models.TextField(verbose_name="Special Message", help_text="The content of the SpecialMessage.xml entry for this MSO. This is a more consistent ad crawl, leave blank for none", blank=True)

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
    startRandomForCrawls = models.BooleanField(verbose_name="StartRandom - Crawls", help_text="If ticked, the STAR will randomly pick a crawl instead of running through them sequentially.", default=False)
    startRandomForGreetings = models.BooleanField(verbose_name="StartRandom - Greetings", help_text="If ticked, the STAR will randomly pick a greeting instead of running through them sequentially.", default=False)
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

    def get_startrandom_crawl(self):
        # COUGH
        if self.startRandomForCrawls:
            return " StartRandom=\"true\""
        else:
            return ""

    def get_startrandom_greeting(self):
        if self.startRandomForGreetings:
            return " StartRandom=\"true\""
        else:
            return ""

    def __str__(self):
        # will look something like "the optiplex i2 (HD XD - N EVERETT-HQ - HD | 013011)"
        return f"{self.friendlyName} ({self.__startype_to_prefix__()}{self.locale}{self.__startype_to_suffix__()} | {self.heId})"

class AffiliateAd(models.Model):
    star = models.ForeignKey(Star, on_delete=models.CASCADE, related_name="affiliate_ads", help_text="The STAR this ad crawl is associated with. Leave blank and tick the 'MSO Crawl' box for an ad crawl that applies to all STARs from this MSO.", blank=True, null=True)
    is_mso_crawl = models.BooleanField(help_text="If ticked, this ad crawl will apply to all STARs from this ad crawl's MSO REGARDLESS of the content of the STAR field. If not ticked, this ad crawl will only apply to the STAR specified in the 'STAR' field. [Mostly Unimplemented]", default=False)
    crawl_content = models.TextField(help_text="The content of the crawl for this ad.", max_length=280)
    friendlyName = models.CharField(max_length=100, help_text="A friendly name for this ad, for your reference.")
    display_from = models.DateTimeField(help_text="The date and time from which this ad should start being displayed on the STAR.", blank=True, null=True)
    display_to = models.DateTimeField(help_text="The date and time after which this ad should stop being displayed on the STAR.", blank=True, null=True)
    dmaCode = models.CharField(max_length=10, help_text="The DMA code that should match for this ad to be displayed. (e.g. 819 for Seattle-Tacoma)", blank=True)
    stateCode = models.CharField(max_length=2, help_text="The state code that should match for this ad to be displayed. (e.g. WA for Washington)", blank=True)

    def __str__(self):
        return f"{self.friendlyName} ({self.star.friendlyName})"
    class Meta:
        verbose_name = "Ad Crawl"

    def get_attributes(self):
        attributes = [""]
        if self.is_mso_crawl:
            attributes.append('MsoCode="' + self.star.mso.code + '"')
        else:
            attributes.append('HeadendId="' + self.star.heId + '"')

        if self.display_from:
            attributes.append('StartDate="' + self.display_from.strftime("%m/%d/%Y") + '"')
            attributes.append('StartTime="' + self.display_from.strftime("%H:%M:%S") + '"')

        if self.display_to:
            attributes.append('EndDate="' + self.display_to.strftime("%m/%d/%Y") + '"')
            attributes.append('EndTime="' + self.display_to.strftime("%H:%M:%S") + '"')

        if self.dmaCode:
            attributes.append('DmaCode="' + self.dmaCode + '"')

        if self.stateCode:
            attributes.append('StateCode="' + self.stateCode + '"')

        return " ".join(attributes)

    def get_main_attribute(self):
        if self.star.startRandomForCrawls:
            return ' StartRandom="true"'

class Greeting(models.Model):
    star = models.ForeignKey(Star, on_delete=models.CASCADE, related_name="greetings")
    line1 = models.CharField(max_length=100, help_text="The first line of the greeting. This should be a short phrase that will be displayed on the STAR's screen.")
    line2 = models.CharField(max_length=100, blank=True, help_text="The second line of the greeting. This should be a short phrase that will be displayed on the STAR's screen.")
    display_from = models.DateTimeField(help_text="The date and time from which this ad should start being displayed on the STAR.", blank=True, null=True)
    display_to = models.DateTimeField(help_text="The date and time after which this ad should stop being displayed on the STAR.", blank=True, null=True)
    dmaCode = models.CharField(max_length=10, help_text="The DMA code that should match for this ad to be displayed. (e.g. 819 for Seattle-Tacoma)", blank=True)
    stateCode = models.CharField(max_length=2, help_text="The state code that should match for this ad to be displayed. (e.g. WA for Washington)", blank=True)


    def __str__(self):
        return f"{self.line1} {self.line2} ({self.star.friendlyName})"

    def linebreak(self):
        if self.line2 and self.line2.strip():
            return f"{self.line1}\\n{self.line2}"
        return self.line1

    def get_attributes(self):
        # Initialize it with a blank thing so we have a space at the start. Jank but it works.
        attributes = [""]
        if self.display_from:
            attributes.append('StartDate="' + self.display_from.strftime("%m/%d/%Y") + '"')
            attributes.append('StartTime="' + self.display_from.strftime("%H:%M:%S") + '"')

        if self.display_to:
            attributes.append('EndDate="' + self.display_to.strftime("%m/%d/%Y") + '"')
            attributes.append('EndTime="' + self.display_to.strftime("%H:%M:%S") + '"')

        if self.dmaCode:
            attributes.append('DmaCode="' + self.dmaCode + '"')

        if self.stateCode:
            attributes.append('StateCode="' + self.stateCode + '"')

        return " ".join(attributes)

class SpecialMessage(models.Model):
    mso = models.ForeignKey(Mso, on_delete=models.CASCADE, related_name="special_messages")
    message = models.TextField(help_text="The content of the entry")

    def __str__(self):
        return f"Special Message for {self.mso.name}"

    def get_attributes(self):
        return 'MsoCode="' + self.mso.code + '"'

class WxDotComPromoText(models.Model):
    star = models.ForeignKey(Star, on_delete=models.CASCADE, related_name="wxpromotexts")
    message = models.TextField(help_text="The content of the promo text")
    display_from = models.DateTimeField(help_text="The date and time from which this ad should start being displayed on the STAR.", blank=True, null=True)
    display_to = models.DateTimeField(help_text="The date and time after which this ad should stop being displayed on the STAR.", blank=True, null=True)
    dmaCode = models.CharField(max_length=10, help_text="The DMA code that should match for this ad to be displayed. (e.g. 819 for Seattle-Tacoma)", blank=True)
    stateCode = models.CharField(max_length=2, help_text="The state code that should match for this ad to be displayed. (e.g. WA for Washington)", blank=True)

    def __str__(self):
        return f"{self.message} ({self.star.friendlyName})"

    class Meta:
        verbose_name = "Azul 7Day Fcst Message"

    def get_attributes(self):
        # Initialize it with a blank thing so we have a space at the start. Jank but it works.
        attributes = [""]
        if self.display_from:
            attributes.append('StartDate="' + self.display_from.strftime("%m/%d/%Y") + '"')
            attributes.append('StartTime="' + self.display_from.strftime("%H:%M:%S") + '"')

        if self.display_to:
            attributes.append('EndDate="' + self.display_to.strftime("%m/%d/%Y") + '"')
            attributes.append('EndTime="' + self.display_to.strftime("%H:%M:%S") + '"')

        if self.dmaCode:
            attributes.append('DmaCode="' + self.dmaCode + '"')

        if self.stateCode:
            attributes.append('StateCode="' + self.stateCode + '"')

        return " ".join(attributes)