from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
import json
from analytics.serializers import PlaceSerializer, CategoryAnalyticsSerializer
from .models import Place, CategoryAnalytics


class PlaceList(APIView):
    def get(self, request):
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)
    # queryset = Place.objects.all()
    # serializer_class = PlaceSerializer
    #
    # def list(self, request, *args, **kwargs):
    #     response = super().list(request, *args, **kwargs)
    #     response.data.pop('count', None)
    #     response.data.pop('next', None)
    #     response.data.pop('previous', None)
    #     return response


# class PlaceDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Place.objects.all()
#     serializer_class = PlaceSerializer


class CategoryAnalyticsList(APIView):
    def get(self, requests):
        checks = CategoryAnalytics.objects.all()
        serializer = CategoryAnalyticsSerializer(checks, many=True)
        return Response(serializer.data)



# class CategoryAnalyticsDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = CategoryAnalytics.objects.all()
#     serializer_class = CategoryAnalyticsSerializer