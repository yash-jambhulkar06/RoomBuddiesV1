from django.db.models import Count, Prefetch, Q

from .models import Conversation, Message


def get_user_conversations(user):
    return (
        Conversation.objects.filter(
            Q(user=user) | Q(provider=user)
        )
        .select_related(
            "room",
            "user",
            "provider",
        )
        .prefetch_related(
            Prefetch(
                "messages",
                queryset=Message.objects.select_related("sender"),
            )
        )
        .annotate(
            unread_count=Count(
                "messages",
                filter=Q(messages__is_read=False)
                & ~Q(messages__sender=user),
            )
        )
        .order_by("-created_at")
    )