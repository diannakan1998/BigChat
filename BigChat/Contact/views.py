# from django.shortcuts import render

# Create your views here.
# import requests
from .models import Contact, Profile
from auth.models import Users
# from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
# from django.core import serializers

def index(request):
     return HttpResponse("Contact POST")

class Contacts(View):

    @classmethod
    def get(self, request):
        token = request.GET.get("token")
        # print(token)
        return JsonResponse(getContact(token))


def getContact(token):
    try:
        user =  Users.objects.get(token=token)
        # print(user.user_id)
        frd = Contact.objects.get(user_id=user.user_id)
        jsonObj = { "contact" : []}

        # print(frd.friend_id)
        for i in frd.friend_id:
            jo = {'name': 1, "email": 1, 'image':1, 'desc':1}
            # fu = Users.objects.get(user_id=i)
            f = Profile.objects.get(email=Users.objects.get(user_id=i).email)
            jo['email'] = f.email
            jo['name'] = f.name
            jo['image'] = f.profile_img_str
            jo['desc'] = f.profile_description
            jsonObj['contact'].append(jo)
        jsonObj['contact'].sort(key=lambda x: x['name'], reverse=False)
        # print(jsonObj)
        return jsonObj
    except Exception as e:
        print(e)
        return {'error': "Failed to get contact."}


class profile(View):

    @classmethod
    def get(self, request):
        email = request.GET.get("email")
        # print(email)
        try:

            user = Profile.objects.get(email=email)
            json = {"email":0, "name":0, "image":0, "desc":0,"error":''}
            json['email'] = user.email
            json['name'] = user.name
            json['image'] = user.profile_img_str
            json['desc'] = user.profile_description
            # print(json)
            return JsonResponse(json)
        except Exception as e:
            print(e)
            return JsonResponse({'error': "Failed to get profile"})

    @classmethod
    def post(self, request):
        try:
            token=request.GET.get("token")
            email = request.GET.get("email")
            image = request.GET.get("image")
            name = request.GET.get("name")
            desc = request.GET.get("desc")

            if email is None:
                token=request.POST.get("token")
                email = request.POST.get("email")
                image = request.POST.get("image")
                name = request.POST.get("name")
                desc = request.POST.get("desc")

            # print(email)
            #print(Users.objects.get(email='austinhe1998@gmail.com').token)

            if email==Users.objects.get(token=token).email:
                user = Profile.objects.filter(email=email)
                if(len(user)==0):
                    newu= Profile(email=email, name=name, profile_img_str=image, profile_description=desc)
                    newu.save()
                else:
                	
                    # print(len(image))

                    if len(image) >1:
                        # print("changed")
                        user[0].profile_img_str = image
                        user[0].save()
                    if name is not None:
                        user[0].name = name
                        user[0].save()
                    if desc is not None:
                        user[0].profile_description = desc
                        user[0].save()
	                
                    # print(user[0].profile_img_str)
                # print("reached")
                return JsonResponse({"email":email, "name":name, "image":image, "desc":desc, "error":''})
            else:
                return JsonResponse({'error':'Cannot change other peoples profile'})
            # print(json)

        except Exception as e:
            print(e)
            return JsonResponse({'error': "Failed to change profile"})

#
