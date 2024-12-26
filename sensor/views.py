import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SensorData, User
from .serializers import SensorDataSerializer
from datetime import datetime

# Variables globales
compteur = 0  # Compteur d'alertes
incident = False  # Indicateur d'incident

# Fonction pour envoyer un message Telegram
def send_telegram_message(chat_id, message):
    telegram_token = '7558130646:AAFtB5ahO9TvHPZmNApNrjWwfjv2D9-nvFg'
    url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print(f"Message envoyé avec succès à {chat_id}")
    else:
        print(f"Erreur lors de l'envoi du message : {response.status_code}")

# Fonction pour envoyer les alertes selon la hiérarchie
def envoyer_alertes_hierarchie(sensor_data):
    global compteur
    message = (
        f"Température : {sensor_data.temp}°C\n"
        f"Date : {sensor_data.date.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Alerte : Température élevée, veuillez vérifier."
    )

    # Récupérer les utilisateurs par niveau d'alerte
    utilisateurs = User.objects.all().order_by('alert_level')

    # Logique des alertes hiérarchiques
    for user in utilisateurs:
        if (user.alert_level == 1 and compteur >= 1) or \
           (user.alert_level == 2 and compteur >= 4) or \
           (user.alert_level == 3 and compteur >= 7):
            personalized_message = f"{message}\nResponsable : {user.name}"
            send_telegram_message(user.telegram_chat_id, personalized_message)

class SensorDataView(APIView):
    """
    API view to handle retrieving and posting sensor data.
    """
    def get(self, request):
        data = SensorData.objects.all()
        serializer = SensorDataSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        global compteur, incident
        print("Données reçues : ", request.data)
        serializer = SensorDataSerializer(data=request.data)

        if serializer.is_valid():
            sensor_data = serializer.save()

            if sensor_data.temp > 20:  # Détection d'incident
                if not incident:
                    incident = True
                    compteur = 0  # Réinitialisation du compteur pour un nouvel incident
                compteur += 1
                envoyer_alertes_hierarchie(sensor_data)
            else:  # Température normale
                incident = False
                compteur = 0

            return Response(serializer.data, status=201)

        print("Erreurs de validation : ", serializer.errors)
        return Response(serializer.errors, status=400)

class LastSensorDataView(APIView):
    """
    API view to retrieve the latest sensor data.
    """
    def get(self, request):
        try:
            last_data = SensorData.objects.latest('date')
            serializer = SensorDataSerializer(last_data)
            return Response(serializer.data)
        except SensorData.DoesNotExist:
            return Response({"error": "Aucune donnée trouvée"}, status=404)

# Vue pour vérifier l'état actuel de l'incident
class IncidentStatusView(APIView):
    def get(self, request):
        global incident, compteur
        if incident:  # Vérifie si un incident est actif
            try:
                last_data = SensorData.objects.latest('date')
                return Response({
                    "incident": True,
                    "start_date": last_data.date.strftime('%Y-%m-%d %H:%M:%S'),
                    "compteur": compteur
                })
            except SensorData.DoesNotExist:
                return Response({
                    "incident": True,
                    "start_date": "Inconnu",
                    "compteur": compteur
                })
        else:
            return Response({"incident": False})