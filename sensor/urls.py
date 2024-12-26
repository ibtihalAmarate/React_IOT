from django.urls import path
from .views import SensorDataView, LastSensorDataView,IncidentStatusView

urlpatterns = [
    path('data/', SensorDataView.as_view(), name='sensor_data'),
    path('data/last/', LastSensorDataView.as_view(), name='last_sensor_data'),
    path('incident/status/', IncidentStatusView.as_view(), name='incident_status'),
]
