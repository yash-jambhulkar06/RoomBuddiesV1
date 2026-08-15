from apps.notifications.models import Notification

def create_notification(
    *,
    user,
    title,
    message,
    notification_type,
):
    """
    Create a notification for a user
    """
    
    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        type=notification_type,
    )
    