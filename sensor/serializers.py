from rest_framework import serializers
from .models import SensorData

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = ['temp', 'hum', 'date']  # Utiliser directement 'temp', 'hum' et 'date'
