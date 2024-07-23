from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    otp_base32 = models.CharField(max_length=200, null=True)
    logged_in = models.BooleanField(default=False)

    # Adding unique related_name arguments to resolve conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='auth_app_user_groups',  # Unique related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='auth_app_user_permissions',  # Unique related_name
        blank=True,
    )

    def __str__(self):
        return str(self.username)
