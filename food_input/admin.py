from django.contrib import admin
from .models import Product, FoodRecord, Measurement, DisplayName, GlucoseValue
from .actions import export_as_csv_action
from .forms import MeasurementForm

@admin.register(FoodRecord)
class FoodRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_id', 'datetime', 'amount', 'display_name', 'product', 'creator')
    product_fields = [str(field.name) for field in FoodRecord._meta.get_fields()][1:]
    actions = [export_as_csv_action("CSV Export", fields=product_fields)]
    list_filter = ('creator', 'patient_id')

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    form = MeasurementForm
    list_display = ('name', 'name_en', 'amount')
    filter_vertical = ('linked_product',)

@admin.register(DisplayName)
class DisplayNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'name', 'name_en')
    list_filter = ('creator', 'product__productgroep_oms')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_omschrijving', 'productgroep_oms', 'occurrence')
    list_filter = ('productgroep_oms',)

@admin.register(GlucoseValue)
class FoodRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_id', 'datetime', 'glucose_value',  'creator')
    product_fields = ['id', 'patient_id', 'datetime', 'glucose_value']
    actions = [export_as_csv_action("CSV Export", fields=product_fields)]
    list_filter = ('creator', 'patient_id')