import uuid

from django.db import models

from addon.models import Post


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="chats")
    user_id = models.CharField(max_length=255)
    peer_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("post", "user_id", "peer_id")


class ChatBot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=255, unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_bot = models.ForeignKey(ChatBot, on_delete=models.CASCADE, related_name="bot_messages", null=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages", null=True)

    sender_side = models.CharField(max_length=255)
    sender_type = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
