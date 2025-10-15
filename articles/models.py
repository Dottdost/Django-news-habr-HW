from django.db import models
from django.contrib.auth.models import User

CATEGORIES = [
    ('programming', 'programming'),
    ('design', 'design'),
    ('science', 'science'),
    ('other', 'other'),
]

class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    image = models.ImageField(upload_to='articles/')
    content = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
