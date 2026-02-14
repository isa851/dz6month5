from django.urls import path
from app.settings.views import HelloAPIVIew

urlpatterns = [
    path("", HelloAPIVIew.as_view(), name='hello')
]
