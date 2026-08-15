from django.urls import path
from .views import notification_list,mark_notification_read

app_name="notifications"

urlpatterns=[
    path(
    "",
    notification_list,
    name="notification_list",
    ),
    
    path("<int:pk>/read/",mark_notification_read,name="mark_notification_read"),
]