from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    
    
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        email=self.normalize_email(email)
        
        user=self.model(
            email=email,
            **extra_fields,
        )
        
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        
        return self.create_user(
            email,
            password,
            **extra_fields,
        )
        
        
class User(AbstractUser):
    
    objects=UserManager()

    class Role(models.TextChoices):
        USER = "USER", "User"
        PROVIDER = "PROVIDER", "Service Provider"

    username = None

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email