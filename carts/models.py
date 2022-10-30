from django.db import models
import uuid
from accounts.models import Account
from core.models import Product


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    def sub_total(self):
        return (self.product.product_price * self.quantity)

    def __str__(self):
        return str(self.product.product_name)

