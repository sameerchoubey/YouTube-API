from django.db import models


class main_db(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    video_id = models.CharField(max_length=200)
    video_title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    published_date = models.DateField()
    thumbnail_url = models.CharField(max_length=200)

    def __str__(self):
        return self.video_title
