import json
import base64
import requests

from django.conf import settings
from django.core.files.base import ContentFile 

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
                "max_tokens" : 1000,
                "response_as_dict": True,
                }

            response = requests.post(url, json=payload, headers=self.headers)
            result = json.loads(response.text)
            logger.info(f'EdenAI Generate Reply Response: {result}')
            return result['openai']['generated_text']
        
        except Exception as e:
            logger.exception(f"Exception on EdenAI generate reply service: {e}")
            raise e

    def generate_image(self, image_description:str) -> ContentFile:
        try:
            url = "https://api.edenai.run/v2/image/generation"              	 
            payload = {
                "providers": "deepai",
                "text": image_description,
                "resolution" : "512x512",
                "num_images": 1
            }

            response = requests.post(url, json=payload, headers=self.headers)
            result = json.loads(response.text)
            byte_data = base64.b64decode(result['deepai']['items'][0]["image"])
            return ContentFile(byte_data, name="recipe.jpg")
        except Exception as e:
            logger.exception(f"Exception on OpenAI generate image service: {e}")
            raise e

