from django.contrib import admin
from .models import Product, FoodRecord, Measurement
from .actions import export_as_csv_action
from .forms import MeasurementForm

@admin.register(FoodRecord)
class FoodRecordAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'datetime', 'amount', 'product', 'creator')
    product_fields = [str(field.name) for field in FoodRecord._meta.get_fields()][1:]
    actions = [export_as_csv_action("CSV Export", fields=product_fields)]
    list_filter = ('creator', 'patient_id')

class MeasurementAdmin(admin.ModelAdmin):
    form = MeasurementForm

admin.site.register(Product)
admin.site.register(Measurement, MeasurementAdmin)