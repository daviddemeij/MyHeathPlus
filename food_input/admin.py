from django.contrib import admin
from .models import Product, FoodRecord, Measurement
from .actions import export_as_csv_action
from .forms import MeasurementForm

@admin.register(FoodRecord)
class FoodRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_id', 'datetime', 'amount', 'product', 'creator')
    product_fields = [str(field.name) for field in FoodRecord._meta.get_fields()][1:]
    actions = [export_as_csv_action("CSV Export", fields=product_fields)]
    list_filter = ('creator', 'patient_id')

class MeasurementAdmin(admin.ModelAdmin):
    form = MeasurementForm
    list_display = ('name', 'amount')
    filter_vertical = ('linked_product',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_omschrijving', 'productgroep_oms', 'occurrence')
    list_filter = ('productgroep_oms',)

admin.site.register(Measurement, MeasurementAdmin)