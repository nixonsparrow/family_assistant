from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from PIL import Image


class Profile(models.Model):
    class Meta:
        ordering = [Lower('user__username')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField('Profile Image', default='default.jpg', upload_to='profile_images')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        width, height = img.size  # get dimensions

        # check which one is smaller
        if height < width:
            # make square by cutting off equal amounts left and right
            left = (width - height) / 2
            right = (width + height) / 2
            top = 0
            bottom = height
            img = img.crop((left, top, right, bottom))

        elif width < height:
            # make square by cutting off bottom
            left = 0
            right = width
            top = 0
            bottom = width
            img = img.crop((left, top, right, bottom))

        if width > 300 and height > 300:
            img.thumbnail((300, 300))

        img.save(self.image.path)
