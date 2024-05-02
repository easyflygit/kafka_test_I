from django.urls import path
from .views import PurchaseCheckAPIView

urlpatterns = [
    # path('api/checks/', CheckView.as_view(), name='check-list'),
    path('api/checks/', PurchaseCheckAPIView.as_view(), name='purchase_check'),
]