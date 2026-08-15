from .models import Notification

def get_user_notifications(user):
    return(
        Notification.objects.filter(user=user).order_by("-created_at")
    )
    
def get_unread_notification_count(user):
    return Notification.objects.filter(
        user=user,
        is_read=False,
    ).count()