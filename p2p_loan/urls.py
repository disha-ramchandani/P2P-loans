"""p2p_loan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.landing_page, name="landing"),
    path('home', user_views.home, name='home'),
    path('getstarted', user_views.getstarted, name='getstarted'),
    path('signup/borrower', user_views.signup_borrower, name='borrower_signup'),
    path('signup/lender', user_views.signup_lender, name='lender_signup'),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),
    path('logout/', user_views.logout_page, name='logout'),
    path('landing/', user_views.landing_page, name='landing_page')
]
