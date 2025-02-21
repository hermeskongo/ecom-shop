"""
URL configuration for ecommerce project.

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import settings
from .views import home

from django.contrib.auth import get_user_model, login
from django.http import HttpResponse


# def good(request):
#    user = get_user_model().objects.get(email='hermes@gmail.com')
#    user.backend = 'django.contrib.auth.backends.ModelBackend'
#    login(request, user)
#    return HttpResponse("User logged in")

# path('good/', good),
urlpatterns = [
        path('admin/', admin.site.urls),
        path('', home, name='home'),
        path('', include('store.urls')),
        path('', include('cart.urls')),
        path('', include('accounts.urls')),
        path('', include('orders.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
