from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
import numpy as np
import os
from PIL import Image

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    gender_choices = (('M','Male'),('F','Female'), ('O','Other'))
    gender = models.CharField(max_length=6, choices = gender_choices, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        sqrWidth = np.ceil(np.sqrt(img.size[0]*img.size[1])).astype(int)
        img_resize = img.resize((sqrWidth, sqrWidth))
        if img_resize.height>300 or img_resize.width>300:
            size=(300,300)
            img_resize.thumbnail(size)
            img_resize.save(self.image.path)

    def __str__(self):
        return f'{self.user.username} Profile'

# Delete the image on deleting the Profile object
@receiver(models.signals.post_delete, sender=Profile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes image from filesystem
    when corresponding `Profile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path) and 'default.jpg' not in instance.image.path:
            os.remove(instance.image.path)

# Delete the old image on changing the profile image
@receiver(models.signals.pre_save, sender=Profile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old image from filesystem
    when corresponding `Profile` object is updated
    with new image.
    """
    if not instance.pk:
        return False

    try:
        old_image = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False

    new_image = instance.image
    if not old_image == new_image:
        if os.path.isfile(old_image.path) and 'default.jpg' not in old_image.path:
            os.remove(old_image.path)

