from django.urls import path
from .views import PurchaseCheckAPIView, CheckView

urlpatterns = [
    path('api/checks/', CheckView.as_view(), name='check-list'),
    path('api/purchase_check/', PurchaseCheckAPIView.as_view(), name='purchase_check'),

]