from django.db import models

class Banknote(models.Model):
    image_base64 = models.TextField(blank=False)