
from openai import OpenAI
import urllib
import os
import requests
import json
import base64
from openai import AsyncOpenAI
from asgiref.sync import sync_to_async
import logging

from django.conf import settings

from users.models import UserProfile
from .db_methods import get_user_from_db, get_prompt_persona

logger = logging.getLogger(__name__)


key="sk-NzehhzYg9CoTyiIc169416F26a1e4f21B9A522159cCb3aAd"
client = AsyncOpenAI(
    api_key=key, 
    base_url="https://api.aiguoguo199.com/v1"
)

async def send_to_gpt(user_message:str, user_id:int) -> str:
    persona_prompt = await get_prompt_persona(user_id)
    response = await client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"{persona_prompt} {user_message}",
        }
    ],
    model="gpt-4o",
)
    text_response = response.choices[0].message.content

    return text_response

@sync_to_async
def generate_one(prompt, name, telegram_id):
    user_profile = UserProfile.objects.get(telegram_id=telegram_id)


    url = "https://api.getimg.ai/v1/stable-diffusion-xl/text-to-image"

    payload = {
        "model": "stable-diffusion-xl-v1-0",
        "prompt": f"{prompt}",
        "width": 1024,
        "height": 1024,
        "steps": 30,
        "guidance": 7.5,
        "seed": 0,
        "scheduler": "euler",
        "output_format": "jpeg",
        "response_format": "url"    
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer key-vwdlSx6i1blWLX4qfMrf4X0yram97XEgeGTrql7OIxD0j20jUg1yrtRXMurx097UfEj75WAWeAK9m1VOnYeYQ8fCJJ4rLCJ"
        }
    
    response = requests.post(url, json=payload, headers=headers)
    response_json = json.loads(response.text)
    image_url = response_json.get("url", "An unknown error occurred.")
    print(image_url)
    return image_url




def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

    
# def generate_one1(prompt, path_folder,name):
    

#     response = client.images.generate(
#         prompt=f"Generate an image based on the following sentence: '{prompt}'. On picture should be human.",
#         n=1,
#         size="1024x1024"
#     )
#     url = response.data[0].url
#     urllib.request.urlretrieve(url,f"{path_folder}/{name}.jpg")
#     return f"{path_folder}/{name}.jpg"
    
# def generate_one(prompt, path_folder, name, telegram_id):
#     user_profile = UserProfile.objects.get(telegram_id=telegram_id)
#     birth = user_profile.date_birth
#     fio = user_profile.fio

#     # url = "https://api.getimg.ai/v1/essential-v2/text-to-image"

#     # payload = {
#     # "style": "photorealism",
#     # "prompt": f"{prompt}. In style of {birth} years",
#     # "aspect_ratio": "1:1",
#     # "output_format": "jpeg",
#     # "response_format": "url"
#     # }

#     url = "https://api.getimg.ai/v1/stable-diffusion-xl/text-to-image"

#     payload = {
#     "model": "stable-diffusion-xl-v1-0",
#     "prompt": f"A photo of young {fio}. which {prompt}. With people.",
#     "negative_prompt": "Old photo.Image with text, blurry, cartoon, interior, Женщина, Девушка, Ковер, Без человека, портрет. Old photo.",
#     "width": 1024,
#     "height": 1024,
#     "steps": 30,
#     "guidance": 7.5,
#     "seed": 0,
#     "scheduler": "euler",
#     "output_format": "jpeg",
#     "response_format": "url"    
#     }

#     headers = {
#     "accept": "application/json",
#     "content-type": "application/json",
#     "authorization": "Bearer key-vwdlSx6i1blWLX4qfMrf4X0yram97XEgeGTrql7OIxD0j20jUg1yrtRXMurx097UfEj75WAWeAK9m1VOnYeYQ8fCJJ4rLCJ"
#         }
    
#     response = requests.post(url, json=payload, headers=headers)
#     response_json = json.loads(response.text)
#     url = response_json.get("url", "An unknown error occurred.")
#     # message = response.text.json().get("url", {}).get("url", "An unknown error occurred.")
#     print(url)
#     urllib.request.urlretrieve(url,f"{path_folder}/{name}.jpg")
#     return f"{path_folder}/{name}.jpg"




# def image_to_base64(image_path):
#     with open(image_path, "rb") as image_file:
#         # Read the image file and encode it to base64
#         encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
#     return encoded_string

# def image_to_image(image_url, telegram_id, name, path_folder):
#     user_profile = UserProfile.objects.get(telegram_id=telegram_id)
#     birth = user_profile.date_birth
#     fio = user_profile.fio
#     media_dir = settings.MEDIA_ROOT
#     image_url = os.path.join(media_dir,f"{image_url}.jpg")
#     encoded_img = image_to_base64(image_url)

#     url = "https://api.getimg.ai/v1/stable-diffusion-xl/image-to-image"

#     payload = {
#     "model": "stable-diffusion-xl-v1-0",
#     "prompt": f"a photo in style {birth} of {fio}. Improve quality.",
#     "negative_prompt": "Disfigured, cartoon, blurry, Старый, Женщина",
#     "image": f"{encoded_img}",
#     "strength": 0.5,
#     "steps": 50,
#     "guidance": 7.5,
#     "seed": 0,
#     "scheduler": "euler",
#     "output_format": "jpeg",
#     "response_format": "url"
#     }
#     headers = {
#     "accept": "application/json",
#     "content-type": "application/json",
#     "authorization": "Bearer key-vwdlSx6i1blWLX4qfMrf4X0yram97XEgeGTrql7OIxD0j20jUg1yrtRXMurx097UfEj75WAWeAK9m1VOnYeYQ8fCJJ4rLCJ"
#     }

#     response = requests.post(url, json=payload, headers=headers)
#     response_json = json.loads(response.text)
#     url = response_json.get("url", "An unknown error occurred.")
#     print(url)
#     urllib.request.urlretrieve(url,f"{path_folder}/{name}.jpg")
#     return f"{path_folder}/{name}.jpg"




