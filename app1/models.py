from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=10)
    address = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


    # if default user name and our app user avoid circular error
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='app1_user_groups',  # unique related_name
        related_query_name='user',
    )

    # if default user name and our app user avoid circular error
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='app1_user_permissions',  # unique related_name
        related_query_name='user_permission',
    )

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Task(models.Model):
    name = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    assigned_to = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return self.assigned_to.username

