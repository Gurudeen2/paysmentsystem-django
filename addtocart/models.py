from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AddToCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name =models.CharField(max_length=20, blank=False)
    image = models.ImageField(upload_to="addtocart/%Y/%m/%d", blank=True)
    price =models.IntegerField()
    ordered = models.BooleanField()

    def __str__(self) -> str:
        return self.product_name
    