from django.contrib import admin
from .forms import FoodRecordForm
# Register your models here.
from .models import Product, FoodRecord

class FoodRecordAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'datetime', 'amount', 'product')


admin.site.register(FoodRecord)