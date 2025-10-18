from django.db import models

from common.models import BaseModel


class OrgType(models.TextChoices):
    UNIVERSITY = 'university', 'University'
    SCHOOL = 'school', 'School'
    PRIVATE_SCHOOL = 'private_school', 'Private School'


class Organization(BaseModel):
    name = models.CharField(max_length=100)
    org_type = models.CharField(max_length=20, choices=OrgType.choices)

    def __str__(self):
        return f"{self.name} ({self.get_org_type_display()})"
    class Meta:
        db_table = 'organizations'

class OrganizationImage(BaseModel):
    organization = models.ForeignKey(Organization,related_name="images",on_delete=models.CASCADE)
    image = models.ImageField(upload_to="organizations/",blank=True,null=True)

    def __str__(self):
        return f"Image for {self.organization.name}"

    class Meta:
        db_table = "organization_image"