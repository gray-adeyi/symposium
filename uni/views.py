from django.views import generics
# Create your views here.


class Login(generics.TemplateView):
    template_name = 'uni/login.html'
