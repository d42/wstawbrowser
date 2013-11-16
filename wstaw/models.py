from django.db import models

class Image(models.Model):
    image_number = models.IntegerField(primary_key=True)
    image_link = models.CharField(max_length=200)
    thumbnail_link = models.CharField(max_length=200)

# Create your models here.
