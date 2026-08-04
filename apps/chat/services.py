from .models import Conversation,Message

def mark_conversation_as_read(conversation,user):
    Message.objects.filter(
        conversation=conversation,
        is_read=False,
    ).exclude(
        sender=user,
    ).update(
        is_read=True
    )