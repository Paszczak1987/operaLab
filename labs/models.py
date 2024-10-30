from django.db import models
from django.template.defaultfilters import default


# Create your models here.
class Laboratory(models.Model):
    
    name = models.CharField(max_length=75, unique=True)
    short_name = models.CharField(max_length=25, unique=True)
    lab_code = models.CharField(max_length=10, default="", unique=True)
    leadership_area = models.CharField(max_length=5, default="")
    
    description = models.TextField(default="", blank=True)
    
    street = models.CharField(max_length=100, default="", blank=True)
    number = models.CharField(max_length=10, default="", blank=True)
    city = models.CharField(max_length=100, default="", blank=True)
    zip_code = models.CharField(max_length=10, default="", blank=True)
    country = models.CharField(max_length=20, default="")
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    contact_email = models.EmailField()
    
    def __str__(self):
        return f"{self.name} ({self.lab_code})"
        
    def __repr__(self):
        return self.short_name
    
    def formatted_address(self):
        return {
            'street': self.street,
            'number': self.number,
            'zip_code': self.zip_code,
            'city': self.city,
            'country': self.country,
        }
        
    class Meta:
        verbose_name_plural = "Laboratories"
    
