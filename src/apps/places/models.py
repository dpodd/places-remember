from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from config.utils import unique_slugify

User = get_user_model()


class Memory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    zoom = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('memory_detail', kwargs={'slug': self.slug})

    def save(self, **kwargs):
        slug_str = "%s" % (self.title,)
        unique_slugify(self, slug_str)
        super().save(**kwargs)