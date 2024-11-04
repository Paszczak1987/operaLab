from django.db import models
from labs.models import Laboratory

# Create your models here.
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
    
    ##############
    # Laboratory #
    
    def attach_laboratory(self, laboratory):
        """Attach manager to laboratory. If manager has technicians attached they will also be attached."""
        """If laboratory has technicians inside they will get manager"""
        self.laboratory = laboratory
        self.save()
        if laboratory:
            laboratory.update_assigned_manager_name()
        if self.has_technicians():
            self._update_technicians_lab()
        if laboratory.has_manager():
            for tech in laboratory.list_technicians():
                tech.attach_manager(self)
    
    def has_laboratory(self):
        return self.laboratory is not None
    
    def get_laboratory(self):
        return f"{self.laboratory!r}" if self.has_laboratory() else None
    
    ###############
    # Technicians #

    def has_technicians(self):
        return self.technicians.exists()
    
    def list_technicians(self):
        return self.technicians.all() if self.has_technicians() else None
   
    def _update_technicians_lab(self):
        for technician in self.technicians.all():
            technician.attach_laboratory(self.laboratory)
   
    
    def retire(self):
        """Detache manager from laboratory and from technicians in it"""
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
    
    ###########
    # Manager #
        
    def attach_manager(self, manager):
        self.manager = manager
        self.save()
    
    def has_manager(self):
        return self.manager is not None
    
    def get_manager(self):
        return f"{self.manager!r}" if self.has_manager() else None
    
    def remove_manager(self):
        self.manager = None
        self.save()
        
    ##############
    # Laboratory #
    
    def attach_laboratory(self, laboratory):
        self.laboratory = laboratory
        self.save()
    
    def has_laboratory(self):
        return self.laboratory is not None
    
    def get_laboratory(self):
        return f"{self.laboratory!r}" if self.has_laboratory() else None
    
    def remove_laboratory(self):
        self.laboratory = None
        self.save()
    

        
        