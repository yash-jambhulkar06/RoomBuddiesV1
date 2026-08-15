from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from .models import Notification

from .selectors import (
    get_user_notifications,
)


@login_required
def notification_list(request):

    notifications = get_user_notifications(
        request.user
    )

    return render(
        request,
        "notifications/notification_list.html",
        {
            "notifications": notifications,
        },
    )
    

@login_required
def mark_notification_read(request,pk):
    notification=get_object_or_404(
        Notification,
        id=pk,
        user=request.user,
    )
    
    notification.is_read= True 
    notification.save()
    
    return redirect("notifications:notification_list")