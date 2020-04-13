from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
import os
from PIL import Image

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='event_pics')
    organizer = models.ForeignKey(User,related_name='o_events', on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, related_name='a_events')
    description = models.CharField(max_length=1500)
    created_on = models.DateTimeField(default=timezone.now)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=100)
    address = models.CharField(max_length=250)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.thumbnail.path)
        if img.height>400 or img.width>625:
            size=(625,400)
            img.thumbnail(size)
            img.save(self.thumbnail.path)

    def __str__(self):
        return self.name

# Delete the thumbnail image on deleting the Event object
@receiver(models.signals.post_delete, sender=Event)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes thumbnail from filesystem
    when corresponding `Event` object is deleted.
    """
    # and 'default.jpeg' not in old_image.path
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)

# Delete the old thumbnail image on changing the event thumbnail image
@receiver(models.signals.pre_save, sender=Event)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old thumbnail from filesystem
    when corresponding `Event` object is updated
    with new thumbnail.
    """
    if not instance.pk:
        return False
    try:
        old_thumbnail = sender.objects.get(pk=instance.pk).thumbnail
    except sender.DoesNotExist:
        return False

    new_thumbnail = instance.thumbnail
    if not old_thumbnail == new_thumbnail:
        if os.path.isfile(old_thumbnail.path):
            os.remove(old_thumbnail.path)