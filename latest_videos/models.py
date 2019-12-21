from django.db import models

# Create your models here.


class main_db(models.Model):
    index = models.IntegerField(primary_key=True, unique=True)
    video_title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    published_date = models.DateField()
    thumbnail_url = models.CharField(max_length=200)
    video_url = models.CharField(max_length=200)

    def __str__(self):
        return self.video_title
