from django.db import models
from labs.models import Laboratory


class Employee(models.Model):
    
    first_name = models.CharField(max_length=100, default="", null=True, blank=True)
    last_name = models.CharField(max_length=100, default="", null=True, blank=True)
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f"{self.pk}: {self.last_name}"

class GroupManager(Employee):
    pass
   
class LabManager(Employee):
    group_manager = models.ForeignKey(
        GroupManager,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lab_managers'
    )
    
    laboratory = models.OneToOneField(
        Laboratory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_manager'
    )
    
    def assign_laboratory(self, laboratory):
        self.laboratory = laboratory
        self.save()
        if laboratory:
            laboratory.update_assigned_manager_name()
        if self.has_technicians():
            self._update_technicians_lab()
    
    def _update_technicians_lab(self):
        for technician in self.technicians.all():
            technician.assign_laboratory(self.laboratory)
    
    def has_laboratory(self):
        return self.laboratory is not None
    
    def get_laboratory(self):
        return f"{self.laboratory!r}" if self.has_laboratory() else None
    
    def has_technicians(self):
        return self.technicians.exists()
    
    def list_technicians(self):
        return self.technicians.all() if self.has_technicians() else None
    
    def retire(self):
        self.laboratory.update_assigned_manager_name(False)
        self.laboratory = None
        self.save()
        if self.laboratory:
            self.laboratory.refresh_from_db()
        if self.has_technicians():
            for technician in self.technicians.all():
                technician.remove_manager()
    
class Technician(Employee):
    manager = models.ForeignKey(
        LabManager,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='technicians'
    )
    
    laboratory = models.ForeignKey(
        Laboratory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='technicians'
    )
    
    def assign_laboratory(self, laboratory):
        self.laboratory = laboratory
        self.save()
        # self.refresh_from_db()
        
    def assign_manager(self, manager):
        self.manager = manager
        self.save()
    
    def has_manager(self):
        return self.manager is not None
    
    def get_manager(self):
        return f"{self.manager!r}" if self.has_manager() else "not assigned"
    
    def remove_manager(self):
        self.manager = None
        self.save()
    
    def has_laboratory(self):
        return self.laboratory is not None
    
    def get_laboratory(self):
        return f"{self.laboratory!r}" if self.has_laboratory() else "not assigned"
    
    def remove_laboratory(self):
        self.laboratory = None
        self.save()
    

        
        