from django.db import models

# Create your models here.
class Audit(models.Model):
    actor = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,)
    action = models.CharField(
        max_length=50)
    target_type = models.CharField(
        max_length=50)
    target_id = models.CharField(
        max_length=100)
    previous_state = models.JSONField(
        null=True,
        blank=True)
    new_state = models.JSONField(
        null=True,
        blank=True)
    reason = models.TextField(
        null=True,
        blank=True)
    metadata = models.JSONField(
        null=True,
        blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
