from django.db import models
from django.urls import reverse


# Each product will have a name, price, optional description, optional image and availability

class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.CharField(max_length=180,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=180, db_index=True)
    image = models.ImageField(upload_to='products/%/%m%d',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # index together to specify an index for id and slug field together. Will be using for querin
    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    # We use get_absolute_url to retrieve a product object
    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.id, self.slug])
