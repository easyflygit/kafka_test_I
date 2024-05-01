from django.urls import path
from .views import PlaceView, CategoryAnalyticsList, CategoryAnalyticsDetail


urlpatterns = [
    path('places/', PlaceView.as_view(), name='place-list'),
    path('analytics/', CategoryAnalyticsList.as_view(), name='analytics-list'),
    path('analytics/<int:pk>/', CategoryAnalyticsDetail.as_view(), name='analytics-detail')
]


