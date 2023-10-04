import json
import base64
import requests
from PIL import Image
from io import BytesIO

from django.conf import settings
from django.core.files.base import ContentFile
from vcamp.apps.user.helpers.image_in_s3 import store_image_in_s3

from vcamp.shared.helpers.logging_helper import logger


class EdenAIService():
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {settings.EDENAI_API_KEY}"}

    def generate_reply(self, instruction:str) -> str:
        try:

            url ="https://api.edenai.run/v2/text/chat"
            payload = {
                "providers": "openai",
                "settings": { "openai": "gpt-4" },
                "text": instruction,
                "chatbot_global_action": "Act as a chef.",
                "previous_history": [],
                "temperature" : 0.0,
                "max_tokens" : 2000,
                "response_as_dict": True,
                }

            response = requests.post(url, json=payload, headers=self.headers)
            result = json.loads(response.text)
            logger.info(f'EdenAI Generate Reply Response: {result}')
            return result['openai']['generated_text']
        
        except Exception as e:
            logger.exception(f"Exception on EdenAI generate reply service: {e}")
            raise e

    def generate_image(self, image_description:str) -> str | None:
        try:
            url = "https://api.edenai.run/v2/image/generation"              	 
            payload = {
                "providers": "replicate",
                "text": image_description,
                "resolution" : "1024x1024",
                "num_images": 1
            }

            response = requests.post(url, json=payload, headers=self.headers)
            result = json.loads(response.text)
            image_data = base64.b64decode(result['replicate']['items'][0]["image"])
            # image = ContentFile(image_data, name="recipe.jpg")
            img = Image.open(BytesIO(image_data)).convert('RGB')
            buffer = BytesIO()
            img.save(buffer, format='JPEG', optimize=True, quality=25)
            image_bytes = buffer.getvalue()
            image_url = store_image_in_s3(image_bytes)
            return image_url
        except Exception as e:
            logger.exception(f"Exception on OpenAI generate image service: {e}")
            return None

