from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError

class AktyorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    ism = serializers.CharField()
    davlat = serializers.CharField()
    jins = serializers.CharField()
    tugilgan_yil = serializers.DateField()

    def validate_ism(self, qiymat):
        if len(qiymat) < 4:
            raise ValidationError("Ism-familiya bunday kalta bo'lmaydi")
        return qiymat

    def validate_jins(self, qiymat):
        if qiymat != 'Erkak' and qiymat != 'Ayol':
            raise ValidationError("Xato")
        return qiymat


class TarifSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nom = serializers.CharField()
    narx = serializers.IntegerField()
    davomiylik = serializers.DurationField()

class IzohSerializer(serializers.Serializer):
    class Meta:
        model = Izoh
        fields = '__all__'
class KinoSerializer(serializers.ModelSerializer):
    aktyorlar = AktyorSerializer(many=True)
    class Meta:
        model = Kino
        fields = '__all__'

class KinoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kino
        fields = '__all__'

    def to_representation(self, instance):
        kino = super(KinoSerializer, self).to_representation(instance)
        kino.update({"aktyorlar_soni": len(kino.get("aktyorlar"))})
        kino.update({"izoh_soni": instance.izoh_set.all().count()})
        return kino

