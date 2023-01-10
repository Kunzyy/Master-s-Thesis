"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from PentestTB import views
from PentestTB.tasks import startupOpenvas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='Home'),
    path('planning', views.planning, name='planning'),
    path('planningConfirm', views.planningConfirm, name='planningConfirm'),
    path('discovery', views.discovery, name='discovery'),
    path('attack', views.attack, name='attack'),
    path('install', views.installTools, name='install'),

    path('registrer', views.register, name='register'),
    path('account', views.account, name='account'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    # Ajax request to get updates from background tasks

    path('ajaxRequest/', views.requestTask, name='ajaxRequest')
]

startupOpenvas()
