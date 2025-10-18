from django.db import models

from apps.Organization.models import Organization
from common.models import BaseModel


class Teacher(BaseModel):
    full_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, unique=True)
    rating = models.FloatField(default=0.0)
    image = models.ImageField(upload_to="teachers/")
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="teachers"
    )

    def __str__(self):
        return f"{self.full_name} ({self.organization.name})"
    class Meta:
        db_table = 'teachers'
