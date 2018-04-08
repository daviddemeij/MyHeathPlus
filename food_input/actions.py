import unicodecsv
from django.http import HttpResponse
from .models import Product, FoodRecord, DisplayName

def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """

    def export_as_csv(modeladmin, request, queryset):
        opts = modeladmin.model._meta

        if not fields:
            field_names = [field.name for field in opts.fields]
        else:
            field_names = fields

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % str(opts).replace('.', '_')

        writer = unicodecsv.writer(response, encoding='utf-8', delimiter='\t')
        if header:
            writer.writerow(field_names)
        for obj in queryset:
            row = [getattr(obj, field)() if callable(getattr(obj, field)) else getattr(obj, field) for field in
                   field_names]
            writer.writerow(row)
        return response

    export_as_csv.short_description = description
    return export_as_csv

def count_occurrence():
    occurrence_list = []
    for product in Product.objects.all():
        occurrence = FoodRecord.objects.filter(product=product.id).count()
        if product.occurrence != occurrence:
            product.occurrence = occurrence
            product.save()
        occurrence_list.append((product.product_omschrijving, occurrence))
    return occurrence_list

def reset_display_names():
    for display_name in DisplayName.objects.all():
        display_name.delete()

    products = Product.objects.all()
    for product in products:
        name = product.product_omschrijving
        if ("- " in name and "- en" not in name):
            pos1 = name.find(" ")
            pos2 = name.find("- ")
            name2 = name[pos1+1].upper()+name[pos1+2:pos2]+name[:pos1].lower()+name[pos2+1:]
            print(name, " => ", name2)
            name = name2
        elif name[-1] == "-":
            pos1 = name.find(" ")
            name2 = name[pos1+1].upper()+name[pos1+2:-1]+name[:pos1].lower()
            print(name, " => ", name2)
            name = name2

        DisplayName.objects.create(product=product, name=name)
