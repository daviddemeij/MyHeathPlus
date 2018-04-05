from django.shortcuts import render, redirect
from .forms import FoodRecordForm
from dal import autocomplete
from django.contrib.auth.decorators import login_required
from .models import Product, FoodRecord, Measurement
from collections import defaultdict

@login_required
def home(request):
    if request.method == 'POST':
        form = FoodRecordForm(request.POST)

        # Link productgroup to measurement unit
        link_measurement = request.POST.get('koppel_eenheid_aan_alle_producten_binnen_deze_categorie')
        category = Product.objects.get(pk=request.POST.get('product')).productgroep_oms
        eenheid = Measurement.objects.get(pk=request.POST.get("eenheid"))
        if link_measurement and category != "<geen categorie>" and eenheid:
            print("adding \"" + str(eenheid) + "\" to product group: " + category)
            form.add_error('eenheid', "\"" + str(eenheid) + "\" succesvol gekoppeld aan productcategorie: " + category)
            products = Product.objects.all().filter(productgroep_oms=category)
            linked_products = eenheid.linked_product.all()
            for product in products:
                if product not in linked_products:
                    eenheid.linked_product.add(product)

        # Process form
        if form.is_valid():
            eenheid = Measurement.objects.get(pk=request.POST.get("eenheid"))
            instance = form.save(commit=False)
            instance.amount = float(request.POST.get("aantal_eenheden")) * eenheid.amount
            instance.measurement = eenheid
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
                instance.save()
        else:
            print("input is not valid!")
    else:
        form = FoodRecordForm()
    food_records = FoodRecord.objects.filter(creator=request.user).order_by('datetime')
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

    return render(request, 'home.html', {'form': form, 'food_records_grouped': dict(food_records_grouped)})

@login_required
def delete_record(request, id):
    record = FoodRecord.objects.filter(pk=id).first()
    if record:
        if record.creator == request.user:
            record.delete()
    return redirect('/')


class ProductAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Product.objects.none()

        qs = Product.objects.all()

        category = self.forwarded.get('categorie', None)

        if category and category != "<geen categorie>":
            qs = qs.filter(productgroep_oms=category)

        if self.q:
            qs = qs.filter(product_omschrijving__contains=self.q)

        return qs

class MeasurementAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Measurement.objects.none()

        qs = Measurement.objects.all()

        product = self.forwarded.get('product')

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        elif product:
            qs = qs.filter(linked_product=product)
        return qs.order_by('amount')

