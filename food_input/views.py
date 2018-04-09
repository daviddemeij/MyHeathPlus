from django.shortcuts import render, redirect
from .forms import FoodRecordForm
from dal import autocomplete
from django.contrib.auth.decorators import login_required
from .models import FoodRecord, Measurement, Product, DisplayName
from collections import defaultdict
from .actions import count_occurrence
import datetime

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

@login_required
def count(request):
    occurrence_list = count_occurrence()
    return render(request, 'count.html', {'occurrence_list': occurrence_list})

@login_required
def home(request):
    selected_patient = FoodRecord.objects.filter(creator=request.user).order_by('-created_at').first().patient_id
    if request.method == 'GET' and convert_int(request.GET.get('copy')):
        food_record = FoodRecord.objects.filter(id=request.GET.get('copy')).first()
        initial_data = {}
        if food_record and request.user == food_record.creator:
            initial_data['patient_id'] = food_record.patient_id
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
        form = FoodRecordForm(initial=initial_data)

    elif request.method == 'POST':
        if request.POST.get('update_eenheden'):
            update_time = convert_time(request.POST.get('update_datetime'))
            update_value = convert_float(request.POST.get('update_eenheden').replace(",", "."))
            food_record = FoodRecord.objects.get(pk=request.POST.get('food_record_id'))
            if food_record and food_record.creator == request.user:
                measurement = food_record.measurement
                if update_value:
                    if measurement.name == "gram":
                        food_record.amount_of_measurements = update_value
                        food_record.amount = update_value
                    else:
                        food_record.amount_of_measurements = update_value
                        food_record.amount = update_value * measurement.amount
                if update_time:
                    food_record.datetime = food_record.datetime.replace(hour=update_time.hour, minute=update_time.minute)
                food_record.save()
            form = FoodRecordForm()
        else:
            form = FoodRecordForm(request.POST)
            print("request ", request.POST.get('patient_id'))
            selected_patient = request.POST.get('patient_id')
            # Process form
            if form.is_valid():
                eenheid = Measurement.objects.get(pk=request.POST.get("eenheid"))
                instance = form.save(commit=False)
                instance.amount = float(request.POST.get("aantal_eenheden")) * eenheid.amount
                instance.measurement = eenheid
                instance.product = DisplayName.objects.get(pk=request.POST.get("display_name")).product
                instance.amount_of_measurements = float(request.POST.get("aantal_eenheden"))
                print(request.POST.get('tijd'))
                date = datetime.datetime.strptime(request.POST.get('datum'), '%Y-%m-%d')
                time = datetime.datetime.strptime(request.POST.get('tijd'), '%H:%M')
                print(time.hour, time.minute)
                instance.datetime = date.replace(hour=time.hour, minute=time.minute)


                # Link productgroup to measurement unit
                link_measurement = request.POST.get('koppel_eenheid_aan_alle_producten_binnen_deze_categorie')
                category = instance.product.productgroep_oms

                if link_measurement and category != "<geen categorie>" and eenheid:
                    print("adding \"" + str(eenheid) + "\" to product group: " + category)
                    form.add_error('eenheid',
                                   "\"" + str(eenheid) + "\" succesvol gekoppeld aan productcategorie: " + category)
                    products = Product.objects.all().filter(productgroep_oms=category)
                    linked_products = eenheid.linked_product.all()
                    for product in products:
                        if product not in linked_products:
                            eenheid.linked_product.add(product)

                if request.POST.get('use_different_name'):
                    if request.POST.get('different_name'):
                        display_name = DisplayName.objects.create(name=request.POST.get('different_name'),
                                                                  product=instance.product,
                                                                  creator=request.user)
                        instance.display_name = display_name
                        mutable = request.POST._mutable
                        request.POST._mutable = True
                        request.POST['display_name'] = display_name.id
                        request.POST._mutable = mutable
                        FoodRecordForm(request.POST)

                if instance.product not in eenheid.linked_product.all():
                    eenheid.linked_product.add(instance.product)
                    form.add_error('eenheid',
                                   "\"" + str(eenheid) + "\" is nu gekoppeld aan: " + str(instance.product))
                instance.creator = request.user
                fields = [field.name for field in FoodRecord._meta.fields + FoodRecord._meta.many_to_many]

                for field in fields:
                    if field.startswith("field_"):
                        nutrition_value = getattr(instance.product, field)
                        if nutrition_value:
                            if "sp" in nutrition_value:
                                nutrition_value = 0.0
                            setattr(instance, field, float(nutrition_value)*(instance.amount / float(instance.product.hoeveelheid)))
                existing_object = FoodRecord.objects.filter(patient_id=instance.patient_id).filter(datetime=instance.datetime).filter(product=instance.product).filter(amount=instance.amount).first()
                if existing_object:
                    print("foodrecord already exists")
                    form.add_error('aantal_eenheden', "Deze log is al eerder ingevoerd in de database.")
                else:
                    product = instance.product
                    product.occurrence += 1
                    product.save()
                    instance.save()
            else:
                print("input is not valid!")
    else:
        form = FoodRecordForm()

    if request.method == 'GET' and convert_int(request.GET.get('select_patient')):
        selected_patient = convert_int(request.GET.get('select_patient'))

    food_records = FoodRecord.objects.filter(patient_id=selected_patient).order_by('datetime')
    food_records_grouped = defaultdict(defaultdict)
    for food_record in food_records:
        date = food_record.datetime.date()
        hour = food_record.datetime.hour
        if hour < 12:
            if 'Ochtend' in food_records_grouped[date]:
                food_records_grouped[date]['Ochtend'].append(food_record)
            else:
                food_records_grouped[date]['Ochtend'] = [food_record]
        elif 12 <= hour < 17:
            if 'Middag' in food_records_grouped[date]:
                food_records_grouped[date]['Middag'].append(food_record)
            else:
                food_records_grouped[date]['Middag'] = [food_record]
        else:
            if 'Avond' in food_records_grouped[date]:
                food_records_grouped[date]['Avond'].append(food_record)
            else:
                food_records_grouped[date]['Avond'] = [food_record]
    patient_list = FoodRecord.objects.all().values("patient_id").distinct()
    return render(request, 'home.html', {'form': form, 'food_records_grouped': dict(food_records_grouped),
                                         'patient_list': patient_list, 'selected_patient': selected_patient})

@login_required
def delete_record(request, id):
    record = FoodRecord.objects.filter(pk=id).first()
    if record:
        if record.creator == request.user:
            product = record.product
            if product.occurrence > 0:
                product.occurrence -= 1
                product.save()
            record.delete()
    return redirect('/')


class ProductAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Product.objects.none()

        qs = DisplayName.objects.all()

        category = self.forwarded.get('categorie', None)

        if category and category != "<geen categorie>":
            qs = qs.filter(product__productgroep_oms=category)

        if self.q:
            for s in self.q.split(" "):
                qs = qs.filter(name__icontains=s) | qs.filter(product__fabrikantnaam__icontains=s)

        return qs.order_by('-product__occurrence')

class MeasurementAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Measurement.objects.none()

        qs = Measurement.objects.all()
        display_name = DisplayName.objects.get(pk=self.forwarded.get('display_name'))
        product = display_name.product

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        elif product:
            qs = qs.filter(linked_product=product)
        return qs.order_by('amount')

