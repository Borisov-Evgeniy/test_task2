from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Discount(models.Model):
    name = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Tax(models.Model):
    name = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, blank=True, null=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, blank=True, null=True)
    stripe_session_id = models.CharField(max_length=100, blank=True, null=True)

    def calculate_total_amount(self):
        total = sum(item.price for item in self.items.all())
        if self.discount:
            total *= (1 - self.discount.percentage / 100)
        if self.tax:
            total *= (1 + self.tax.rate / 100)
        return round(total, 2)

    def save(self, *args, **kwargs):
        self.total_amount = self.calculate_total_amount()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.pk} - {self.user.username} - ${self.total_amount}"