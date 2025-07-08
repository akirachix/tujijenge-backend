from django.db import models

class Order(models.Model):
    order_id =  models.AutoField(primary_key=True)
    mamamboga = models.ForeignKey(
        "users.Mamamboga",         
        on_delete=models.CASCADE,
        related_name='orders'
    )
    product = models.ForeignKey(
        "stock.Product",
        on_delete=models.CASCADE,
        related_name='orders'
    )
    community = models.ForeignKey(
        "communities.Community",
        on_delete=models.CASCADE,
        related_name='orders',
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    deadline_at = models.DateTimeField(null=True, blank=True)
    order_date = models.DateTimeField(null=True, blank=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.mamamboga.first_name}"


