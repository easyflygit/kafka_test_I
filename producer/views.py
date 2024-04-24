from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Check
from .serializers import CheckSerializer


class CheckView(APIView):
    def post(self, request):
        serializer = CheckSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)