import json

from django.http import JsonResponse
from django.views import View


class BlankView(View):

    def get(self, request):
        return JsonResponse({}, safe=False, status=200)

    def post(self, request, hash=None):

        data = request.body
        try:
            data = json.loads(data)
        except Exception as e:
            return JsonResponse({
                "error": "Invalid data"
            }, safe=False, status=400)

        return JsonResponse({}, safe=False, status=200)
