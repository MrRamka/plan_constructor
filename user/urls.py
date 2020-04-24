from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.urls import path

from user import views

urlpatterns = [

    url(r'register/', views.SignUp.as_view(), name='signup'),
    url(r'login/', LoginView.as_view(template_name='user/login.html'), name='login')

]
