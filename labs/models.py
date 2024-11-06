from django.db import models
from django.apps import apps
from django.utils.http import urlencode

# Create your models here.
class Laboratory(models.Model):
    
    name = models.CharField(
        max_length=75,
        unique=True,
        error_messages={
            'unique': "This name already exists."
        }
    )
    short_name = models.CharField(
        max_length=25,
        unique=True,
        error_messages={
            'unique': "This name already exists."
        }
    )
    lab_code = models.CharField(
        max_length=10,
        default="",
        unique=True,
        error_messages={
            'unique': "This code already exists."
        }
    )
    leadership_area = models.CharField(max_length=5, default="")
    
    description = models.TextField(default="", blank=True)
    
    street = models.CharField(max_length=100, default="", blank=True)
    number = models.CharField(max_length=10, default="", blank=True)
    city = models.CharField(max_length=100, default="", blank=True)
    zip_code = models.CharField(max_length=10, default="", blank=True)
    country = models.CharField(max_length=20, default="")
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    manager = models.CharField(max_length=100, default="not assigned", blank=True, null=True)
    contact_email = models.EmailField()
    
    group_manager = models.ForeignKey(
        'personnel.GroupManager',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='laboratories',
        default=None
    )
    
    class Meta:
        verbose_name_plural = "Laboratories"
    
    def import_group_manager_model(self):
        group_manager = apps.get_model('personnel', 'GroupManager')
        return group_manager.objects.get(laboratories=self)
    
    def update_assigned_manager_name(self, assignment=True):
        if assignment:
            self.manager = f"{self.assigned_manager.first_name} {self.assigned_manager.last_name}"
        else:
            self.manager = "not assigned"
        self.save()
        self.refresh_from_db()
        
    def has_manager(self):
        return self.manager != 'not assigned'
    
    def get_manager(self):
        return f"{self.manager}" if self.has_manager() else None
    
    def has_technicians(self):
        return self.technicians.exists()
    
    def list_technicians(self):
        return list(self.technicians.all()) if self.has_technicians() else []
        
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
    
    def has_gps_coordinates(self):
        return bool(None not in [self.latitude, self.longitude])
    
    def has_postal_address(self):
        return bool("" not in [self.street, self.number, self.zip_code, self.city])

    def google_map_url(self):
        if self.has_gps_coordinates():
            base_url = 'https://www.google.com/maps/search/'
            coordinates = f"{self.latitude},{self.longitude}"
            query = urlencode({'api': 1, 'query': coordinates})
            return f"{base_url}?{query}"
        if self.has_postal_address():
            base_url = 'https://www.google.com/maps/search/'
            address_parts = [self.street, self.number, self.zip_code, self.city, self.country]
            address = ', '.join(filter(None, address_parts))
            query = urlencode({'api': 1, 'query': address})
            return f"{base_url}?{query}"
    
    def google_map_url_2(self):
        base_url = 'https://www.google.com/maps/search/'
        return f"{base_url}?api=1&query={self.latitude},{self.longitude}"
    
    