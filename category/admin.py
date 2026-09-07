from django.contrib import admin
from.models import Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug', 'min_order_quantity', 'sold_individually')
    list_editable = ('min_order_quantity', 'sold_individually')

admin.site.register(Category, CategoryAdmin)
