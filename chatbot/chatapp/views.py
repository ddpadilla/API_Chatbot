from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
from decouple import config
from .models import Periodo, Evento, Examen, RequisitosGraduacion, FechasImportantes, Mensajes
from .serializers import (
    PeriodoSerializer, EventoSerializer, ExamenSerializer, RequisitosGraduacionSerializer, FechasImportantesSerializer,
    MensajesSerializer
)
from fuzzywuzzy import fuzz


client = OpenAI(api_key=config("OPENAI_API_KEY"))

KEYWORDS = [
    "fecha", "inicio", "final", "examen", "periodo", "semestre", "vacaciones",
    "calendario", "inscripción", "finalización", "entrega", "receso", "clases",
    "plazo", "convocatoria", "prórroga", "horario", "suspensión", "requisitos",
    "feriado", "feriados", "festivo", "festivos", "matrículas", "matricula",
    "inducción", "graduación", "suficiencia", "grado", "título", "diploma", "certificado",
    "requisito", "actividad", "cupos"
]


def is_question_valid(pregunta):
    pregunta_lower = pregunta.lower()
    return any(fuzz.partial_ratio(pregunta_lower, keyword) > 80 for keyword in KEYWORDS)


def generar_contexto():
    return {
        "periodo": PeriodoSerializer(Periodo.objects.all(), many=True).data,
        "evento": EventoSerializer(Evento.objects.select_related("periodo").all(), many=True).data,
        "examen": ExamenSerializer(Examen.objects.select_related("periodo").all(), many=True).data,
        "requisitos_graduacion": RequisitosGraduacionSerializer(
            RequisitosGraduacion.objects.select_related("periodo").all(), many=True
        ).data,
        "fechas_importantes": FechasImportantesSerializer(
            FechasImportantes.objects.select_related("periodo").all(), many=True
        ).data,
    }


class ConsultasView(APIView):
    def post(self, request):
        pregunta = request.data.get('pregunta')
        if not pregunta:
            return Response({"error": "Se requiere una pregunta."}, status=status.HTTP_400_BAD_REQUEST)

        if not is_question_valid(pregunta):
            return Response({"error": "La pregunta no está relacionada con el calendario académico."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            context = generar_contexto()
            response = client.chat.completions.create(
                messages=[
                    {"role": "system",
                     "content": "Eres un asistente estudiantil que proporciona información sobre calendarios académicos."},
                    {"role": "user", "content": f"Calendario académico: {context}. {pregunta}"}
                ],
                model="gpt-4o-mini",
            )
            respuesta = response.choices[0].message.content.strip()

            # Guardar en la sesión (pila)
            if 'historial' not in request.session:
                request.session['historial'] = []
            request.session['historial'].append({"pregunta": pregunta, "respuesta": respuesta})
            request.session.modified = True

            # Guardar también en el modelo para persistencia
            Mensajes.objects.create(pregunta=pregunta, respuesta=respuesta)

            return Response({"respuesta": respuesta}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error al procesar la solicitud: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HistorialPilaView(APIView):
    def get(self, request):
        historial = request.session.get('historial', [])
        return Response({"historial": historial}, status=status.HTTP_200_OK)

    def post(self, request):
        nueva_entrada = request.data.get('consulta')
        if not nueva_entrada:
            return Response({"error": "Se requiere una consulta para agregar al historial."},
                            status=status.HTTP_400_BAD_REQUEST)

        if 'historial' not in request.session:
            request.session['historial'] = []

        request.session['historial'].append(nueva_entrada)
        request.session.modified = True

        return Response({"message": "Consulta agregada al historial."}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        historial = request.session.get('historial', [])
        if not historial:
            return Response({"error": "El historial está vacío."}, status=status.HTTP_404_NOT_FOUND)

        ultima_entrada = historial.pop()
        request.session['historial'] = historial
        request.session.modified = True

        return Response({"message": "Última consulta eliminada.", "eliminada": ultima_entrada},
                        status=status.HTTP_200_OK)


