"""rivia_soft URL Configuration

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
import django
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from companies.views import home_selfassesment_tracker

urlpatterns = [
    path('', home_selfassesment_tracker),
    path('companies/', include('companies.urls'), name='companies'),
    path('u/', include('users.urls')),
    path('admin/', admin.site.urls, name='admin'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handler page
handler400 = 'error_handler.views.handle_400_error'
handler403 = 'error_handler.views.handle_403_error'
handler404 = 'error_handler.views.handle_404_error'
handler500 = 'error_handler.views.handle_500_error'

# Change admin titles and headers
admin.site.site_header = "Rivia Solutions"
admin.site.site_title = "Rivia Solutions Administration"
admin.site.index_title = "Welcome to RSA"
