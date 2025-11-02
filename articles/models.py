from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

CATEGORIES = [
    ('backend', 'Backend'),
    ('frontend', 'Frontend'),
    ('AI', 'AI'),
    ('cyber-security', 'Cyber security'),
    ('cyber-sport', 'Cyber sport'),
    ('game-development', 'Game Development'),
]


class Article(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('PENDING', 'Pending Review'),
        ('PUBLISHED', 'Published'),
    )

    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    content = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    avg_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.title

    def calculate_rating(self):
        """
         логика:
        Рейтинг = лайки - дизлайки.
        Например:
            5 лайков и 2 дизлайка -> рейтинг = 3.
            Если добавится еще 1 лайк -> рейтинг = 4.
        """
        self.avg_rating = self.likes - self.dislikes
        self.save(update_fields=['avg_rating'])

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Article"
        verbose_name_plural = "Articles"


class Bookmark(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('article', 'user')
        verbose_name = "Bookmark"
        verbose_name_plural = "Bookmarks"

    def __str__(self):
        return f"{self.user} → {self.article}"


class Vote(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    value = models.SmallIntegerField()  # 1 или -1
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('article', 'user')
        verbose_name = "Vote"
        verbose_name_plural = "Votes"

    def __str__(self):
        status = "Like" if self.value == 1 else "DisLike"
        return f"{self.user} {status} {self.article}"

    def save(self, *args, **kwargs):
        existing = Vote.objects.filter(article=self.article, user=self.user).first()
        if existing and existing.pk != self.pk:
            if existing.value != self.value:
                if self.value == 1:
                    self.article.likes += 1
                    self.article.dislikes = max(0, self.article.dislikes - 1)
                else:
                    self.article.dislikes += 1
                    self.article.likes = max(0, self.article.likes - 1)
                self.article.calculate_rating()
                existing.delete()
        else:
            if self.value == 1:
                self.article.likes += 1
            else:
                self.article.dislikes += 1
            self.article.calculate_rating()

        super().save(*args, **kwargs)
        self.article.save(update_fields=['likes', 'dislikes', 'avg_rating'])
