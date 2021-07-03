from rest_framework.views import APIView
from rest_framework.response import Response
from .services import get_top_films


class MainPageView(APIView):

    def get(self, request, *args, **kwargs):
        data = get_top_films()
        return Response(data)