from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count

# Create your models here.

class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=200, blank=True)
    price           = models.DecimalField(max_digits=8, decimal_places=2)  # напр. 2.49 лв./€
    images          = models.ImageField(upload_to = 'photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    # минимум само за този продукт; празно = важи минимумът на категорията
    min_order_quantity_override = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name='минимална поръчка (бр.)',
        help_text='Остави празно, за да важи минимумът на категорията.',
    )
    created_date    = models.DateTimeField(auto_now_add=True) # or auto_add_now=True
    modified_date   = models.DateTimeField(auto_now = True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    @property
    def min_order_quantity(self):
        """Минимумът на продукта, ако е зададен; иначе този на категорията."""
        if self.min_order_quantity_override:
            return max(1, self.min_order_quantity_override)
        return max(1, self.category.min_order_quantity)

    @property
    def has_custom_minimum(self):
        return bool(self.min_order_quantity_override)

    @property
    def order_step(self):
        """Стъпка на бутоните + / - в количката: 1 бр. за твърд алкохол, иначе минималното количество."""
        if self.category.sold_individually:
            return 1
        return self.min_order_quantity
    
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

class VariationManager(models.Manager):
    def extras(self):
        return super(VariationManager, self).filter(variation_category='extra', is_active=True)
    
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

variation_category_choice = (
    ('extra', 'extra'),
    ('size', 'size'),
)

class Variation(models.Model):
    product             = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category  = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value     = models.CharField(max_length=100)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
    

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank = True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products/', max_length=255)

    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'