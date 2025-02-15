"""
URL configuration for erpsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.shortcuts import render
from .views import test_404


def home(request):
    """홈 페이지 렌더링"""
    return render(request, 'home.html')  # ✅ `templates/home.html` 렌더링

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stock/',include('stock.urls')),
    path('',home,name='home'),
    #path('test-404/', test_404),
]

handler404 = 'erpsite.views.custom_page_not_found_view'