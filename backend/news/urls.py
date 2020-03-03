from django.urls import path

from . import views

app_name = 'news'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.ProfileView.as_view(), name='profile'),
]
