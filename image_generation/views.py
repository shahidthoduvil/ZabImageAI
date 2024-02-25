from django.shortcuts import render,redirect
from openai import OpenAI
from .models import AiImage
from django.core.files.base import ContentFile
import os
from django.conf import settings
import json
import requests

api_key=settings.OPEN_API_KEY
client = OpenAI(api_key=api_key)

def generate_image_text(request):

    if api_key is not None and request.method=='POST':
        user_input=request.POST.get('user_input')
        recent_images = AiImage.objects.filter(prompt=user_input).order_by('-id')[:4]
        response=client.images.generate(
            prompt=user_input,
            model="dall-e-2",
            size="1024x1024",
            quality="standard",
        )
        print(response)
        json_response = json.dumps(response, default=lambda o: o.__dict__, indent=2)
        parsed_response = json.loads(json_response)
        print(json_response)

        if 'data' in json_response:
                image_url = parsed_response['data'][0]['url']
                print(image_url)

                if image_url:
                    image_response = requests.get(image_url)

                    ai_image = AiImage(prompt=user_input)
                    ai_image.image.save(f"{user_input}_image.png", ContentFile(image_response.content))
                    ai_image.save()

                    return render(request, 'main.html', {'ai_image': ai_image})
                else:
                    print("Image URL not found in the response.")
        else:
            print("Key 'data' not found in the response.")
    else:
           recent_images = AiImage.objects.all().order_by('-id')[:4]
    
    return render(request,'main.html',{'recent_images':recent_images})





