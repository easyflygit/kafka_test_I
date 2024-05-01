from django.urls import path
from .views import PlaceList, PlaceDetail, CategoryAnalyticsDetail, CategoryAnalyticsList


urlpatterns = [
    path('places/', PlaceList.as_view(), name='place-list'),
    path('places/<int:pk>/', PlaceDetail.as_view(), name='place-detail'),
    path('analytics/', CategoryAnalyticsList.as_view(), name='analytics-list'),
    path('analytics/<int:pk>/', CategoryAnalyticsDetail.as_view(), name='analytics-detail')
]


