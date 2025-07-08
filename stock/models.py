from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal



class Product(models.Model):

    CATEGORY_CHOICES=(
        ('VEG','Vegetable'),
        ('FRUIT','Fruit')
    )
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    unit = models.CharField(max_length=10)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    product_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'), message="Price must be positive")]
    )
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.product_name

class Stock(models.Model):
    stock_id = models.AutoField(primary_key=True)
    mamamboga = models.ForeignKey(
        "users.Mamamboga",
        on_delete=models.CASCADE,
        related_name='stocks',
        null=True,
        blank=True,
        to_field='id'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    last_sync_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return f"Stock {self.stock_id} for {self.mamamboga.mamamboga_name}"