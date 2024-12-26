from django.contrib import admin
from django.urls import path, include
from .views import ReactAppView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('sensor.urls')),  # Inclut les URLs de l'application 'sensor'
      path('', ReactAppView.as_view(), name='home'),
]
