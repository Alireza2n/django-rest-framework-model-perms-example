from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=200)
