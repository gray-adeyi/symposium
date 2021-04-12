from django.db import models

# Create your models here.


class SiteInfo(models.Model):
    """
    Model holds all the information about
    The symposium website

    Note: This models should only have one instance.
    a `SiteInfo.objects.get` method is used in the
    view.py which breaks if multiple instance is
    returned.
    """
    name = models.CharField(max_length=100,
                            help_text="Name of the website")
    favicon = models.FileField()
    apple_icon = models.ImageField(blank=True)
    logo = models.ImageField()
    source_code_link = models.URLField(blank=True)
    about = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if SiteInfo.objects.count() > 1:
            return
        super(SiteInfo, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class SocialAccount(models.Model):
    """
    This model holds all the
    social accout info for the
    site.
    """
    SOCIAL_MEDIA_OPTIONS = (
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('whatsapp', 'Whatsapp'),
        ('telegram', 'Telegram'),
        ('tik_tok', 'Tik Tok'),
    )
    site = models.ForeignKey(SiteInfo,
                             on_delete=models.CASCADE,
                             related_name='social_accounts')
    account = models.CharField(max_length=100, choices=SOCIAL_MEDIA_OPTIONS)
    link = models.URLField()

    def __str__(self):
        return self.account
