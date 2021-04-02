from django.db import models

# Create your models here.


class Firer(models.Model):
    number = models.CharField(max_length=100, null=True, unique=True)
    name = models.CharField(max_length=100, null=True)
    rank = models.CharField(max_length=100, null=True)
    coy = models.CharField(max_length=100, null=True)
    unit = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.number
