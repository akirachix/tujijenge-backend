from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):

   product_id = models.CharField(max_length=5, primary_key=True)
   product_name = models.CharField(max_length=50)
   unit = models.CharField(max_length=10)
   category = models.ForeignKey(
    Category, on_delete=models.CASCADE)
   description = models.TextField(null=True, blank=True)
   product_price = models.DecimalField(max_digits=10, decimal_places=2)
   created_at = models.DateTimeField(auto_now_add=True)
   tags = models.ManyToManyField(Tag, blank=True)




   def __str__(self):
       return self.product_name



class Stock(models.Model):

   stock_id = models.CharField(max_length=5, primary_key=True)
#    "users.mamamboga" = models.ForeignKey(
#        Mamamboga,
#        on_delete=models.CASCADE,
#        related_name='stocks'
#    )

   price = models.DecimalField(max_digits=10, decimal_places=2)
   quantity = models.DecimalField(max_digits=10, decimal_places=2)
   last_updated = models.DateTimeField(null=True, blank=True)
   expiration_date = models.DateTimeField(null=True, blank=True)
   last_sync_at = models.DateTimeField(null=True, blank=True)
   created_at = models.DateTimeField(auto_now_add=True)




   def __str__(self):
       return f"Stock {self.stock_id} for {self.mamamboga.mamamboga_name}"




