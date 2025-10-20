from django.contrib.auth.models import AbstractUser
from django.db import models
from common.models import BaseModel


class UserRoles(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    USER = 'user', 'User'

class User(AbstractUser, BaseModel):
    username = models.CharField( max_length=150,unique=True,null=True,blank=True)
    email = models.EmailField(unique=True, db_index=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True, db_index=True)
    phone_code = models.CharField(max_length=10, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=10,choices=UserRoles.choices,default=UserRoles.USER,)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username or f"User {self.pk}"