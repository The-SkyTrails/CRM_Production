# notification_utils.py

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification


def create_notification(employee, message):
    notification = Notification.objects.create(
        employee=employee,
        name=message,
        is_seen=False,
    )
    notification.save()


def send_notification(employee_id, message, current_count):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(employee_id),
        {"type": "notify", "message": message, "count": current_count},
    )


def assign_notification(employee_id, message, current_count):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(employee_id),
        {"type": "assign", "message": message, "count": current_count},
    )
