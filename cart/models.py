from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator
from stock.models import Product

class Cart(models.Model):
    mamamboga = models.ForeignKey(
        "users.Mamamboga",         
        on_delete=models.CASCADE,
        related_name='carts'
    )   
    session_id = models.CharField(max_length=100, null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.mamamboga and hasattr(self.mamamboga, 'user'):
            return f"Cart for User: {self.mamamboga.user.username}"
        elif self.session_id:
            return f"Cart for Session: {self.session_id}"
        else:
            return "Cart (unknown owner)"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'), message="Quantity must be positive")]
    )

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in cart"
    class Meta:
        unique_together = ('cart', 'product')
    @property
    def total_price(self):
        return self.quantity * self.product.product_price