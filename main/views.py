from django.views import generic
from django.shortcuts import render
from . import models
import logging

logger = logging.getLogger(__name__)


class About(generic.TemplateView):
    template_name = "main/about.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['site_info'] = models.SiteInfo.objects.get()
        return ctx


def handler404(request, exception):
    logger.error("Could not resolve path: ", str(exception.get('path')))
    return render(request, 'main/404.html')


def handler500(request):
    return render(request, 'main/500.html')
