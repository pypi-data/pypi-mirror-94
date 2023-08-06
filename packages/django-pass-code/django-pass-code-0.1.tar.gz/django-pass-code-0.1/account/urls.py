from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('verify/', views.verify, name='verify'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
]
