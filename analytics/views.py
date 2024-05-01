from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
import json
from analytics.serializers import PlaceSerializer, CategoryAnalyticsSerializer
from .models import Place, CategoryAnalytics


class PlaceList(generics.ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data.pop('count', None)
        response.data.pop('next', None)
        response.data.pop('previous', None)
        return response


class PlaceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class CategoryAnalyticsList(generics.ListCreateAPIView):
    queryset = CategoryAnalytics.objects.all()
    serializer_class = CategoryAnalyticsSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data.pop('count', None)
        response.data.pop('next', None)
        response.data.pop('previous', None)
        return response


class CategoryAnalyticsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CategoryAnalytics.objects.all()
    serializer_class = CategoryAnalyticsSerializer