import unicodecsv
from django.http import HttpResponse
from .models import Product, FoodRecord, DisplayName, Measurement
from collections import defaultdict, OrderedDict
import datetime

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
    return sorted(occurrence_list, key=lambda tuple: tuple[1], reverse=True)

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

def convert_int(s):
    try:
        value = int(s)
        return value
    except:
        return False

def convert_float(s):
    try:
        value = float(s)
        return value
    except ValueError:
        return False

def convert_time(s):
    try:
        validtime = datetime.datetime.strptime(s, "%H:%M")
        return validtime
    except:
        return False

def group_food_records(food_records):
    food_records_grouped = OrderedDict()
    for food_record in food_records.order_by('-datetime'):
        date = food_record.datetime.date()
        hour = food_record.datetime.hour
        if date in food_records_grouped:
            food_records_grouped[date]['total']['field_01001'] += float(food_record.field_01001)
            food_records_grouped[date]['total']['field_05001'] += float(food_record.field_05001)
            food_records_grouped[date]['total']['field_02002'] += float(food_record.field_02002)
            food_records_grouped[date]['total']['field_03001'] += float(food_record.field_03001)
        else:
            food_records_grouped[date] = OrderedDict()
            food_records_grouped[date]['Avond'] = []
            food_records_grouped[date]['Middag'] = []
            food_records_grouped[date]['Ochtend'] = []
            food_records_grouped[date]['total'] = OrderedDict()

            food_records_grouped[date]['total']['field_01001'] = float(food_record.field_01001)
            food_records_grouped[date]['total']['field_05001'] = float(food_record.field_05001)
            food_records_grouped[date]['total']['field_02002'] = float(food_record.field_02002)
            food_records_grouped[date]['total']['field_03001'] = float(food_record.field_03001)

        if hour < 12:
            food_records_grouped[date]['Ochtend'].append(food_record)
        elif 12 <= hour < 17:
            food_records_grouped[date]['Middag'].append(food_record)
        else:
            food_records_grouped[date]['Avond'].append(food_record)
    return food_records_grouped

def select_date_patient(request):
    selected_patient = 0
    selected_date = datetime.datetime.now().date()
    created_food_records = FoodRecord.objects.filter(creator=request.user).order_by('-created_at')
    if created_food_records:
        selected_patient = created_food_records.first().patient_id
        selected_date = created_food_records.first().datetime.date()

    if request.method == 'POST':
        if request.POST.get('patient_id'):
            selected_patient = request.POST.get('patient_id')
        if request.POST.get('select_date') and request.POST.get('select_date') == "ALL":
            selected_date = "ALL"
        elif request.POST.get("datum"):
            selected_date = datetime.datetime.strptime(request.POST.get("datum"), '%Y-%m-%d').date()

    if request.method == 'GET':
        if convert_int(request.GET.get('select_patient')):
            selected_patient = convert_int(request.GET.get('select_patient'))
            created_food_records = FoodRecord.objects.filter(patient_id=selected_patient).order_by('-created_at')
            if not request.GET.get('select_date') and created_food_records:
                selected_date = created_food_records.first().datetime.date()
        elif request.GET.get('copy'):
            copied_food_record = FoodRecord.objects.filter(id=request.GET.get('copy')).first()
            selected_patient = copied_food_record.patient_id
            selected_date = copied_food_record.datetime.date()
        if request.GET.get('select_date'):
            date_request = request.GET.get('select_date')
            if date_request == "ALL":
                selected_date = "ALL"
            else:
                selected_date = datetime.datetime.strptime(date_request, '%Y-%m-%d').date()

    return selected_date, selected_patient

def copy_food_record(food_record):
    initial_data = {}
    if food_record:
        if food_record.display_name:
            initial_data['display_name'] = food_record.display_name
        else:
            initial_data['display_name'] = DisplayName.objects.filter(product=food_record.product).first()

        if food_record.measurement:
            initial_data['eenheid'] = food_record.measurement
            if food_record.amount_of_measurements:
                initial_data['aantal_eenheden'] = food_record.amount_of_measurements
            else:
                initial_data['aantal_eenheden'] = food_record.amount / food_record.measurement.amount
        else:
            initial_data['eenheid'] = Measurement.objects.filter(name="gram").first()
            initial_data['aantal_eenheden'] = food_record.amount
    return initial_data

def calculate_nutrition(instance):
    fields = [field.name for field in FoodRecord._meta.fields + FoodRecord._meta.many_to_many]
    for field in fields:
        if field.startswith("field_"):
            nutrition_value = getattr(instance.product, field)
            if nutrition_value:
                if "sp" in nutrition_value:
                    nutrition_value = 0.0
                setattr(instance, field,
                        float(nutrition_value) * (instance.amount / float(instance.product.hoeveelheid)))
    return instance