from django.urls import path
from . views import ConsultasView, HistorialPilaView

urlpatterns = [
    path('pregunta', ConsultasView.as_view(), name='consultas'),
    path('historial', HistorialPilaView.as_view(), name='historial'),
]


