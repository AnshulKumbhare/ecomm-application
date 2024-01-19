from django.contrib import admin
from ecomm_app.models import product 
# Register your models here.

# admin.site.register(product)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'pdetails', 'category', 'is_active']
    list_filter = ['category', 'is_active']
                

admin.site.register(product,ProductAdmin)  #doubt