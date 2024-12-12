"""
URL configuration for EmergencyKonnect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth.password_validation import password_changed
from django.urls import path
from django.contrib.auth import views as auth_views
    
from emergency import views
from emergency.views import passwordsChangeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('signup/', views.register, name='signup'),

    path('accounts/login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),

    path('services/request_service/<str:service_name>/', views.request_view, name='request_service'),
    path('password/', passwordsChangeView.as_view(template_name= 'password_changed.html')),
    path('password_succes/', views.password_success, name='password_success'),

    path('info/<str:username>', views.info, name='info'),
    path('update_request/<int:user_id>/', views.update_request, name='update_request'),  # Update view
    path('delete/<int:user_id>/', views.delete_request, name='delete'),  # Delete vi


]
