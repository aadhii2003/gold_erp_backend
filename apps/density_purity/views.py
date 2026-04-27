from rest_framework import viewsets
from rest_framework import serializers
from .models import DensityPurity

class DensityPuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = DensityPurity
        fields = '__all__'

class DensityPurityViewSet(viewsets.ModelViewSet):
    queryset = DensityPurity.objects.all().order_by('density')
    serializer_class = DensityPuritySerializer
