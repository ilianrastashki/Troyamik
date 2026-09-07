from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)
    # търговия на едро - минимално количество за поръчка от тази категория
    min_order_quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='минимална поръчка (бр.)',
        help_text='Най-малкият брой, който клиентът може да поръча от продукт в тази категория.',
    )

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name
    