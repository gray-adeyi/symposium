from django.urls import path
from . import views

app_name = "uni"

urlpatterns = [
    path('template/', views.GTemplate.as_view(),),
    path('', views.Login.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('activate/<slug:link>/', views.Activate.as_view(), name='activate'),
    path('send-reset-link/', views.SendPasswordReset.as_view(),
         name='reset-link'),
    path('reset/<slug:link>/', views.PasswordReset.as_view(), name='reset'),
    path('class-heads/authorize/',
         views.LeaderAuthorization.as_view(), name='leader-authorize'),
    path('class/create/', views.CreateSymposium.as_view(),
         name='create-class'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('profile/update-user-info/', views.updated_user_info,
         name='update-user-info'),
    path('profile/add-number/', views.add_phone_number,
         name='add-number'),
    path('profile/remove-number/<str:id>/', views.remove_phone_number,
         name='remove-number'),
    path('class-groups/expore/', views.ExploreSymposium.as_view(),
         name='explore-classes'),
    path('class-groups/join/<str:pk>/', views.join_symposium,
         name='join-class'),
    path('FAQs/', views.FAQView.as_view(), name='faqs'),
]
