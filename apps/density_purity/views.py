from rest_framework import viewsets
from rest_framework import serializers
from .models import DensityPurity
from apps.users.models import UserLog

class DensityPuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = DensityPurity
        fields = '__all__'

class DensityPurityViewSet(viewsets.ModelViewSet):
    queryset = DensityPurity.objects.all().order_by('density')
    serializer_class = DensityPuritySerializer

    def perform_create(self, serializer):
        entry = serializer.save()
        UserLog.objects.create(
            user=self.request.user,
            role=self.request.user.role,
            action="CREATE_MATRIX_ENTRY",
            details=f"Added Density: {entry.density}, Purity: {entry.purity}%"
        )
        
    def perform_destroy(self, instance):
        UserLog.objects.create(
            user=self.request.user,
            role=self.request.user.role,
            action="DELETE_MATRIX_ENTRY",
            details=f"Removed Density: {instance.density}, Purity: {instance.purity}%"
        )
        instance.delete()
