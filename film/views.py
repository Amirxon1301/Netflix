from rest_framework.filters import OrderingFilter
from rest_framework import status

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import *

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from rest_framework.pagination import PageNumberPagination
from django.contrib.postgres.search import TrigramSimilarity

from .models import *
from .serializers import *

class HelloAPI(APIView):
    def get(self, request):
        d = {
            "xabar" : "Salom, dunyo",
            "izoh" : "sinov"
        }
        return Response(d)

    def post(self, request):
        d = request.data
        natija = {
            "xabar" : "Post qabul qilindi",
            "post ma'lumoti" : d
        }
        return Response(natija)

class AktyorlarAPI(APIView):
    def get(self, request):
        aktyorlar = Aktyor.objects.all()
        qidiruv = request.query_params.get("qidiruv")
        if qidiruv:
            aktyorlar = Aktyor.objects.annotate(
                oxshashlik = TrigramSimilarity('ism', qidiruv)
            ).filter(oxshashlik__gt=0.5).order_by("-oxshashlik")
        pagination_class = PageNumberPagination
        pagination_class.page_size = 1
        paginator = PageNumberPagination()
        natija = paginator.paginate_queryset(aktyorlar, request)
        serializer = AktyorSerializer(natija, many=True)

        return Response(serializer.data)


    def post(self, request):
        aktyor = request.data
        serializer = AktyorSerializer(data=aktyor)
        if serializer.is_valid():
            data = serializer.validated_data
            Aktyor.objects.create(
                ism = data.get("ism"),
                davlat= data.get("davlat"),
                jins= data.get("jins"),
                tugilgan_yil= data.get("tugilgan_yil"),
            )
            return Response(serializer.data)
        return Response(serializer.errors)

class AktyorAPI(APIView):
    def get(self, request, pk):
        aktyor = Aktyor.objects.get(id=pk)
        serializer = AktyorSerializer(aktyor)
        return Response(serializer.data)

    def update(self, request, pk):
        aktyor = Aktyor.objects.get(id=pk)
        serializer = AktyorSerializer(aktyor, data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            Aktyor.objects.filter(id=pk).update (
                ism = data.get("ism"),
                davlat= data.get("davlat"),
                jins= data.get("jins"),
                tugilgan_yil= data.get("tugilgan_yil"),
            )
            return Response(serializer.data)
        return Response(serializer.errors)


class TariflarAPI(APIView):
    def get(self, request):
        tarif = Tarif.objects.all()
        serializer = TarifSerializer(tarif, many=True)

        return Response(serializer.data)
    def post(self, request):
        tarif = request.data
        serializer = TarifSerializer(data=tarif)
        if serializer.is_valid():
            data = serializer.validated_data
            Tarif.objects.create(
                ism=data.get("ism"),
                davlat=data.get("davlat"),
                jins=data.get("jins"),
                tugilgan_yil=data.get("tugilgan_yil"),
            )
            return Response(serializer.data)
        return Response(serializer.errors)

class TarifAPI(APIView):
    def delete(self, request, pk):
        Tarif.objects.get(id=pk).delete()
        return Response({"successful" : "True"})

    def update(self, request, pk):
        tarif = Tarif.objects.get(id=pk)
        serializer = TarifSerializer(data=tarif)
        if serializer.is_valid():
            data = serializer.validated_data
            Tarif.objects.filter(id=pk).update(
                ism=data.get("ism"),
                davlat=data.get("davlat"),
                jins=data.get("jins"),
                tugilgan_yil=data.get("tugilgan_yil"),
            )
            return Response(serializer.data)
        return Response(serializer.errors)

class KinolarAPI(APIView):
    def post(self, request):
        kino = request.data
        serializer = KinoPostSerializer(data=kino)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def get(self, request):
        kinolar = Kino.objects.all()
        serializer = KinoSerializer(kinolar, many=True)
        return Response(serializer.data)


class KinoAPI(APIView):
    def get(self, request, pk):
        kino = Kino.objects.get(id=pk)
        serializers = KinoSerializer(kino)
        return Response(serializers.data)

class IzohModelViewSet(ModelViewSet):
    queryset = Izoh.objects.all()
    serializer_class = IzohSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['id', 'sana' ]

class IzohListCreateAPI(ListCreateAPIView):
    serializer_class = IzohSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Izoh.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class IzohDeleteAPI(DestroyAPIView):
    queryset = Izoh.objects.all()
    serializer_class = IzohSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            return Response(status=status.HTTP_204_NO_CONTENT)





