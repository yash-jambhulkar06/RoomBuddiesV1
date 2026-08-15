from .selectors import get_unread_notification_count

def notification_count(request):
    if request.user.is_authenticated:
        return{
            "notification_count":get_unread_notification_count(
                request.user
                )
        }
        
    return{
        "notification_count":0
    }