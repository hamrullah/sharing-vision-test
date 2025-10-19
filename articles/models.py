# articles/models.py
from django.db import models

class Post(models.Model):
    class Status(models.TextChoices):
        PUBLISH = "publish", "Publish"
        DRAFT = "draft", "Draft"
        TRASH = "trash", "Trash"

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100, choices=Status.choices)

    class Meta:
        db_table = "posts"          # sesuai permintaan
        ordering = ["-created_date"]

    def __str__(self):
        return f"{self.id} - {self.title[:30]}"
