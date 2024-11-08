from django.core.exceptions import ValidationError
from django.db import models
from labs.models import Laboratory
from .utils import remove_diacritical_marks


# Create your models here.
class Employee(models.Model):
    
    first_name = models.CharField(max_length=100, default="", null=True, blank=True)
    last_name = models.CharField(max_length=100, default="", null=True, blank=True)
    username = models.CharField(max_length=100, default="", null=True, blank=True)
    
    phone_number = models.CharField(max_length=100, default="", null=True, blank=True)
    email = models.EmailField(max_length=100, default="", null=True, blank=True)
    
    class Meta:
        abstract = True
    
    def _generate_unique_username(self, *args, **kwargs):
        # If username is not given, generate username automatically.
        if not self.username:
            # Get rid of non Unicode characters
            created_username = f"{self.last_name[:4].lower()}_{self.first_name[:3].lower()}"
            self.username = remove_diacritical_marks(created_username)
            # Assure username uniqueness (add number, if such username already exist)
            counter = 1
            original_username = self.username
            while type(self).objects.filter(username=self.username).exists():
                self.username = f"{original_username}_{counter}"
                counter += 1
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f"{self.pk}: {self.last_name}"

class Group(models.Model):
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
        
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"Group {self.code}"
        super().save(*args, **kwargs)
        
    def clean(self):
        if not (10 <= self.code <= 99):
            raise ValidationError({'code': 'Code must be a two-digit number between 10 and 99.'})
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(code__gte=10) & models.Q(code__lte=99),
                name='code_must_be_two_digit'
            ),
        ]

class Director(Employee):
    pass

class GroupManager(Employee):
    director = models.ForeignKey(
        Director,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="group_managers",
    )
    
    def save(self, *args, **kwargs):
        self._generate_unique_username()
        super().save(*args, **kwargs)
   
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
    
    def save(self, *args, **kwargs):
        self._generate_unique_username()
        super().save(*args, **kwargs)
    
    ##############
    # Laboratory #
    
    def take_over_the_lab(self, laboratory):
        """Attach manager and his technicians to laboratory.
        If laboratory has technicians attached they will get manager."""
        if not laboratory.has_manager():
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
    
    def leave_the_lab(self):
        """Detache manager from laboratory and from technicians in it."""
        self.laboratory.update_assigned_manager_name(False)
        self.laboratory = None
        self.save()
        if self.laboratory:
            self.laboratory.refresh_from_db()
        if self.has_technicians():
            for technician in self.technicians.all():
                technician.remove_manager()
   
    # Laboratory #
    ##############
    
    ###############
    # Technicians #
    
    def has_technicians(self):
        return self.technicians.exists()
    
    def list_technicians(self):
        return self.technicians.all() if self.has_technicians() else None
   
    def _update_technicians_lab(self):
        for technician in self.technicians.all():
            technician.take_over_the_lab(self.laboratory)
   
    # Technicians #
    ###############
    
    #################
    # Group manager #
    
    def attach_supervisor(self, group_manager):
        self.group_manager = group_manager
        self.save()
    
    def has_supervisor(self):
        return self.group_manager is not None
    
    def get_supervisor(self):
        return self.group_manager if self.has_supervisor() else None
    
    def remove_supervisor(self):
        self.group_manager = None
        self.save()
        
    # Group manager #
    #################
    
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
    
    def save(self, *args, **kwargs):
        self._generate_unique_username()
        super().save(*args, **kwargs)
    
    ###########
    # Manager #
        
    def attach_manager(self, manager):
        self.manager = manager
        self.save()
    
    def has_manager(self):
        return self.manager is not None
    
    def get_manager(self):
        return self.manager if self.has_manager() else None
    
    def remove_manager(self):
        self.manager = None
        self.save()
        
    # Manager #
    ###########
        
    ##############
    # Laboratory #
    
    def attach_laboratory(self, laboratory):
        self.laboratory = laboratory
        self.save()
    
    def has_laboratory(self):
        return self.laboratory is not None
    
    def get_laboratory(self):
        return self.laboratory if self.has_laboratory() else None
    
    def remove_laboratory(self):
        self.laboratory = None
        self.save()
    
    # Laboratory #
    ##############

        
        