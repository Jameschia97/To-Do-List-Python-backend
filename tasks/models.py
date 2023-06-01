from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    completed = models.BooleanField(default=False)
    file = models.FileField(upload_to='documents/',blank = True, null = True)
    
    
    def __str__(self):
        return self.name + ' ' + self.description
    
