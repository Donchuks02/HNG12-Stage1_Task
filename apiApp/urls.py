from django.urls import path
from .views import ClassifyNumberAPIView

urlpatterns = [
    path('api/classify-number/', ClassifyNumberAPIView.as_view(), name='classify-number'),
]
