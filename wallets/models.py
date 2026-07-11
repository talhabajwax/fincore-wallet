from django.db import models

class Wallet(models.Model):
    
   STATUS_CHOICES = [("active", "Active"), ("frozen", "Frozen"), ("expired", "Expired")]
   user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="wallets")
   balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
   status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
   currency = models.CharField(max_length=3, default="PKR")
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)