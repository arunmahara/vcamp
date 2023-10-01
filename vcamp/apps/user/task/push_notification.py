from celery import shared_task
from firebase_admin import messaging, firestore

from vcamp.shared.helpers.logging_helper import logger
from vcamp.apps.user.helpers.authenticate import firebase_app


firestore.client(app=firebase_app)


@shared_task(name = "sendPushNotification")
def sendPushNotification(title: str, msg: str, tokens: list, image: str = "", dataObject=None) -> None:
    try: 
        message = messaging.MulticastMessage(
            data={
                'title':title,
                'body':msg,
                'icon':image,
                'click_action':'https://www.ramailo.tech'
            },
            notification=messaging.Notification(
                title=title,
                body=msg,
                image=image
            ),
            tokens=tokens
        )
        messaging.send_multicast(message)
        return
    except Exception as e:
        logger.error(f"Error while sending push notification: {e}")
        return