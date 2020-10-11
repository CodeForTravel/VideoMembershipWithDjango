
from django.urls import path
from . import views
from videomembership.views import HomeView
app_name = 'users'
urlpatterns = [
    path('user_profile/',views.ProfileView.as_view(),name="user_profile"),
    path('',HomeView.as_view(),name="home")

]
