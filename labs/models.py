from django.db import models

# Create your models here.
class Laboratory(models.Model):
    name = models.CharField(max_length=25)
    short_name = models.CharField(max_length=4)
    
    location = models.CharField(max_length=100)
    country = models.CharField(max_length=20, default="None")
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    leadership_area = models.CharField(max_length=5, default="None")
    
    contact_email = models.EmailField()
    
    def __str__(self):
        return f"{self.name} ({self.short_name})"
        
    def __repr__(self):
        return self.short_name
    
    def formatted_address(self):
        address_split = self.location.split(' ')
        return {
            'street': " ".join(address_split[:3]),
            'city': " ".join(address_split[3:]),
            'country': self.country,
        }
        
    
    class Meta:
        verbose_name_plural = "Laboratories"
    
