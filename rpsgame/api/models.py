from django.db import models
from django.db import models

# ayushg Test-123
class GameUser(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.name
