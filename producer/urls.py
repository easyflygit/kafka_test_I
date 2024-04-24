from django.urls import path
from .views import PurchaseCheckAPIView, CheckView

urlpatterns = [
    path('checks/', CheckView.as_view(), name='check-list'),
    path('purchase_check/', PurchaseCheckAPIView.as_view(), name='purchase_check'),

]