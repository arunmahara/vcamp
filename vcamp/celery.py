import os
from celery import Celery
from celery.schedules import crontab
from .settings import TIME_ZONE


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vcamp.settings')

app = Celery('vcamp')
app.conf.timezone = TIME_ZONE


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks([
    "vcamp.apps.user.task.generate_meal.generate_and_save_recipe",
    "vcamp.apps.user.task.generate_meal.generate_and_save_shopping_list",
    "vcamp.apps.user.task.generate_meal.generate_and_save_meal_plan_with_shopping_list",
    "vcamp.apps.user.task.push_notification.sendPushNotification",
])

app.conf.broker_transport_options = {
    'max_retries': 1,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.2,
}

app.conf.beat_schedule = {
    # 'update_in_every_2_min': {
    #     'task': 'update_status',
    #     'schedule': 2 * 60   # Run every 2 min
    # }, 
}