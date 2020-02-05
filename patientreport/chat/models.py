
from django.db import models

class Room(models.Model):
    label = models.SlugField(unique=True)
    name = models.TextField()

    def __unicode__(self):
        return self.label


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    username = models.TextField()
    message = models.TextField(max_length=3000)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
