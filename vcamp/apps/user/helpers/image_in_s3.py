import uuid
import boto3
import mimetypes

from django.conf import settings
from django.core.files.base import ContentFile
from vcamp.shared.helpers.logging_helper import logger


def store_image_in_s3(image_data: bytes) -> str | None:
    try:
        filename = str(uuid.uuid4()) + '.jpg'
        object_key = "public-images/" + filename

        content_type, _ = mimetypes.guess_type(filename)

        s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        # s3.upload_fileobj(ContentFile(image_data), bucket_name, filename)  //for downloadable file
        s3.upload_fileobj(ContentFile(image_data), bucket_name, object_key, ExtraArgs={'ContentType': content_type})

        image_url = f'https://{bucket_name}.s3.amazonaws.com/{object_key}'
        return image_url
    
    except Exception as e:
        logger.exception(f"Exception while storing image in s3: {e}")
        return None
