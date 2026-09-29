from django.db import models
from django.contrib.auth.models import User

    
class Task(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        blank=True,
        null=True,
    )
    PROJECT_CHOICES = [
        ('studies', 'Studies'),
        ('projects', 'Projects'),
        ('personal', 'Personal'),
    ]
    
    PRIORITY_CHOICES = [
        ('short', 'Short'),
        ('average', 'Average'),
        ('high', 'High'),
    ]

    name = models.CharField(max_length=200, default="Undefined")
    description = models.TextField(blank=True, null=True)
    project = models.CharField(max_length=50, choices=PROJECT_CHOICES, default='studies')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='short')
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name