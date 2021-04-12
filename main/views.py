from django.views import generic
from . import models
# Create your views here.


class About(generic.TemplateView):
    template_name = "main/about.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['site_info'] = models.SiteInfo.objects.get()
        return ctx
