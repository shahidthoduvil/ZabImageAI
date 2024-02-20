from django.db import models

# Create your models here.


class AiImage(models.Model):
    prompt=models.CharField(max_length=200)
    image=models.ImageField(upload_to='images')

    def __str__(self) -> str:
        return str(self.prompt)
    
