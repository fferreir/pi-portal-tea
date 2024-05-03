from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

class PublishedManager(models.Manager):
        def get_queryset(self):
            return super(PublishedManager, self).get_queryset().filter(status='publicado')

class Post(models.Model):
    STATUS_CHOICES = (
        ('rascunho', 'Rascunho'),
        ('publicado', 'Publicado'),
    )

    ESTABLISHMENT_CHOICES = (
        ('bar', 'Bar'),
        ('restaurante', 'Restaurante'),
        ('clube', 'Clube'),
        ('saloes', 'Salões de eventos'),
    )
    CITY_AREA_CHOICES = (
        ('leste', 'Leste'),
        ('oeste', 'Oeste'),
        ('norte', 'Norte'),
        ('sul', 'Sul'),
        ('centro', 'Centro'),
    )
    name = models.CharField(max_length=200)
    kind_of_establishment = models.CharField(max_length=200,
                                             choices=ESTABLISHMENT_CHOICES,
                                             default='bar')
    slug = models.SlugField(max_length=200, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')
    lighting_control_environment = models.BooleanField(default=False)
    soundproof_environment = models.BooleanField(default=False)
    preferential_access = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    description = models.TextField(default='descrição dos serviços do estabelcimento')
    address = models.CharField(max_length=250)
    number = models.CharField(max_length=20)
    neighborhood = models.CharField(max_length=200)
    city_area = models.CharField(max_length=50,
                                 choices=CITY_AREA_CHOICES,
                                 default='centro')
    zip_code = models.DecimalField(max_digits=8, decimal_places=0)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=(STATUS_CHOICES),
                              default='rascunho')
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day, self.slug])

    def __str__(self):
        return self.name


