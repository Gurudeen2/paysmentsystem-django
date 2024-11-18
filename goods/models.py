from django.db import models

# Create your models here.

class Goods(models.Model):
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="order/%Y/%m/%d", blank=True)
    price = models.IntegerField()

    def __str__(self) -> str:
        return self.name