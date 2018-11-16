from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.generic import View

from .models import media


def index(request):
    return HttpResponse("binaryTesting Index")

class binaryMessages(View):
    @classmethod
    def get(self, request):
        print ("Inside get")
        try:
            user_id = request.GET.get("token")
            mediaModel = Media.filter.get(user_id=user_id)

            return FileResponse(mediaModel.mediab)
        except Exception as e:
            print (e)
            return JsonResponse({"error": "something...", "status": 900})

    @classmethod
    def post(self, request):
        print("Inside post")
        try:
            print(request.POST['user_id'])
            user_id = request.POST['user_id']
            print ("got user_id = " + user_id)
            print(request.POST['media'])
            media = request.FILES['media']
            print ("got media")

            mediaModel = None
            if not Media.filter.get(user_id=user_id).exists():
                mediaModel = media(user_id=user_id)
                mediaModel.save()
            else:
                mediaModel = Media.filter.get(user_id=user_id)

            mediaModel.mediab = media
            mediaModel.save()

            return JsonResponse({"success":"saved...", "status": 200})

        except Exception as e:
            print (e)
            return JsonResponse({"error": "something...", "status": 900})
