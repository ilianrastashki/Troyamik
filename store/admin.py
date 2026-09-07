from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductGallery
from django.db.models.functions import Lower
import admin_thumbnails

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'minimum', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInline]

    @admin.display(description='мин. поръчка', ordering='min_order_quantity_override')
    def minimum(self, obj):
        if obj.has_custom_minimum:
            return f'{obj.min_order_quantity} бр. (за продукта)'
        return f'{obj.min_order_quantity} бр. (от категорията)'

    # азбучна подредба (Lower() -> и продукти с малка буква застават на място)
    ordering = (Lower('product_name'),)

    # търсачка: по име, описание и име на категория
    search_fields = ('product_name', 'description', 'category__category_name')
    search_help_text = 'Търсене по име на продукт, описание или категория.'

    list_filter = ('category', 'is_available')
    list_per_page = 25

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active', )
    list_filter = ('product', 'variation_category', 'variation_value', 'is_active')

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)