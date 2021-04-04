from django.urls import path
from . import views

app_name = "uni"

urlpatterns = [
    path('', views.GTemplate.as_view(),),
    path('register/', views.Register.as_view(), name='register'),
    path('activate/<slug:link>', views.Activate.as_view(), name='activate'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('send-reset-link/', views.SendPasswordReset.as_view(),
         name='reset-link'),
    path('reset/', views.PasswordReset.as_view(), name='reset'),
    path('class-heads/authorize/',
         views.LeaderAuthorization.as_view(), name='leader-authorize'),
    path('class/create/', views.CreateSymposium.as_view(),
         name='create-class'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('profile/', views.Profile.as_view(), name='profile'),
]
