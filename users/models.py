from django.db import models
from .manager import UserManager
from django.contrib.auth.models import AbstractBaseUser
import uuid

# Create your models here.
class User(AbstractBaseUser):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(verbose_name="first name", max_length=250, default=True, unique=False)
    last_name = models.CharField(verbose_name="last name", max_length=250, default=True, unique=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
        )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "users"
        
