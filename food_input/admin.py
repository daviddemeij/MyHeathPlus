from django.contrib import admin
from .forms import FoodRecordForm
# Register your models here.
from .models import Product, FoodRecord
from django.http import HttpResponse, HttpResponseForbidden
from .actions import export_as_csv_action


class FoodRecordAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'datetime', 'amount', 'product')
    product_fields = [str(field.name) for field in FoodRecord._meta.get_fields()][1:]
    actions = [export_as_csv_action("CSV Export", fields=product_fields)]

admin.site.register(FoodRecord, FoodRecordAdmin)
admin.site.register(Product)