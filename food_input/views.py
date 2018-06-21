from django.shortcuts import render, redirect
from .forms import FoodRecordForm, CopyMealForm, GlucoseValueForm, UserCreationForm
from dal import autocomplete
from django.contrib.auth.decorators import login_required
from .models import FoodRecord, Measurement, Product, DisplayName, GlucoseValue
from .actions import count_occurrence, convert_int, convert_float, convert_time, group_food_records, \
    select_date_patient, copy_food_record, calculate_nutrition, convert_datetime
import datetime
from django.contrib.auth import login, authenticate

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def home(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/foodlog')
    else:
        form = UserCreationForm()
    return render(request, 'home.html', {'form': form})

@login_required
def count(request):
    if request.user.is_staff:
        occurrence_list = count_occurrence()
        return render(request, 'count.html', {'occurrence_list': occurrence_list})
    else:
        return redirect('/')

@login_required
def foodlog(request):
    print("ID = ", request.user.id)
    if request.method == 'GET' and convert_int(request.GET.get('copy')):
        food_record = FoodRecord.objects.filter(id=request.GET.get('copy')).first()
        initial_data = copy_food_record(food_record)

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
                    if update_time == "?":
                        food_record.missing_time = True
                    else:
                        food_record.missing_time = False
                        food_record.datetime = food_record.datetime.replace(hour=update_time.hour, minute=update_time.minute)
                food_record.save()
            form = FoodRecordForm()
        elif request.POST.get('copy_date'):
            form = FoodRecordForm()
            copy_date = datetime.datetime.strptime(request.POST.get('copy_date'), '%Y-%m-%d')
            time = datetime.datetime.strptime(request.POST.get('copy_time'), '%H:%M')
            for food_record in request.POST.get('food_records').split(",")[:-1]:
                record = FoodRecord.objects.get(pk=int(food_record))
                record.pk = None
                record.creator = request.user
                record.datetime = copy_date.replace(hour=time.hour, minute=time.minute)
                record.created_at = datetime.datetime.now()
                existing_object = FoodRecord.objects.filter(patient_id=record.patient_id).filter(
                    datetime=record.datetime).filter(product=record.product).filter(amount=record.amount).first()
                if existing_object:
                    print("foodrecord already exists")
                else:
                    record.save()
        else:
            form = FoodRecordForm(request.POST)
            # Process form
            if form.is_valid():
                eenheid = Measurement.objects.get(pk=request.POST.get("eenheid"))
                instance = form.save(commit=False)
                instance.amount = float(request.POST.get("aantal_eenheden")) * eenheid.amount
                instance.measurement = eenheid
                instance.product = DisplayName.objects.get(pk=request.POST.get("display_name")).product
                instance.amount_of_measurements = float(request.POST.get("aantal_eenheden"))
                date = datetime.datetime.strptime(request.POST.get('datum'), '%Y-%m-%d')
                time = datetime.datetime.strptime(request.POST.get('tijd'), '%H:%M')
                instance.datetime = date.replace(hour=time.hour, minute=time.minute)
                if not request.user.is_staff:
                    instance.patient_id = convert_int(request.user.id)

                # Link productgroup to measurement unit
                link_measurement = request.POST.get('koppel_eenheid_aan_alle_producten_binnen_deze_categorie')
                category = instance.product.productgroep_oms

                if request.user.is_staff and link_measurement and category != "<geen categorie>" and eenheid:
                    print("adding \"" + str(eenheid) + "\" to product group: " + category)
                    form.add_error('eenheid',
                                   "\"" + str(eenheid) + "\" succesvol gekoppeld aan productcategorie: " + category)
                    products = Product.objects.all().filter(productgroep_oms=category)
                    linked_products = eenheid.linked_product.all()
                    for product in products:
                        if product not in linked_products:
                            eenheid.linked_product.add(product)

                if request.user.is_staff and request.POST.get('use_different_name'):
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

                if instance.product not in eenheid.linked_product.all() and request.user.is_staff:
                    eenheid.linked_product.add(instance.product)
                    form.add_error('eenheid',
                                   "\"" + str(eenheid) + "\" is nu gekoppeld aan: " + str(instance.product))
                instance.creator = request.user
                instance = calculate_nutrition(instance)

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

    selected_date, selected_patient = select_date_patient(request)
    form.initial['patient_id'] = selected_patient

    if not request.user.is_staff:
        food_records = FoodRecord.objects.filter(creator=request.user)
    else:
        food_records = FoodRecord.objects.filter(patient_id=selected_patient)

    dates = food_records.order_by('datetime').values("datetime").distinct()
    date_list = []
    for date in dates:
        if date["datetime"].date() not in date_list:
            date_list.append(date["datetime"].date())

    if selected_date != "ALL":
        form.initial['datum'] = selected_date
        food_records_date = food_records.filter(
            datetime__year=selected_date.year,
            datetime__month=selected_date.month,
            datetime__day=selected_date.day
        )
        if not food_records_date:
            selected_date = "ALL"
        else:
            food_records = food_records_date


    food_records_grouped = group_food_records(food_records)

    patient_list = FoodRecord.objects.all().values("patient_id").distinct()


    return render(request, 'foodlog.html', {'form': form, 'copy_form': CopyMealForm(),
                                         'food_records_grouped': sorted(food_records_grouped.items(), reverse=True),
                                         'patient_list': patient_list, 'selected_patient': selected_patient,
                                         'date_list': reversed(date_list), 'selected_date': selected_date})

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
    if request.GET.get('select_date') and request.GET.get("select_patient"):
        return redirect('/?select_date='+request.GET.get('select_date')+"&select_patient="+request.GET.get("select_patient"))
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
        product = False
        qs = Measurement.objects.all()
        if self.forwarded.get('display_name'):
            display_name = DisplayName.objects.get(pk=self.forwarded.get('display_name'))
            product = display_name.product

        if self.q:
            for s in self.q.split(" "):
                qs = qs.filter(name__icontains=s) | qs.filter(amount__icontains=s)
        elif product:
            qs = qs.filter(linked_product=product)
        return qs.order_by('amount')

@login_required()
def upload_glucose(request):
    if request.POST:
        if request.FILES and request.POST.get('patient_id'):
            csvfile = request.FILES['csv_file']
            for row in csvfile:
                row_decoded = row.decode("utf-8").split("\t")
                if len(row_decoded) >= 3:
                    date, glucose = convert_datetime(row_decoded[1]), convert_float(row_decoded[3])
                    if date and glucose > 0.0:
                        existing_object = GlucoseValue.objects.filter(patient_id=request.user.id).filter(
                            datetime=date).first()
                        if not existing_object:
                            GlucoseValue.objects.create(datetime=date, glucose_value=glucose,
                                                        patient_id=request.user.id, creator=request.user)
        elif request.POST.get("datum") and request.POST.get("tijd") and request.POST.get("glucose_value"):
            datum = datetime.datetime.strptime(request.POST.get('datum'), '%Y-%m-%d')
            tijd = datetime.datetime.strptime(request.POST.get('tijd'), '%H:%M')
            date = datum.replace(hour=tijd.hour, minute=tijd.minute)

            existing_object = GlucoseValue.objects.filter(patient_id=request.user.id).filter(datetime=date).first()
            if not existing_object:
                GlucoseValue.objects.create(datetime=date, glucose_value=request.POST.get("glucose_value"),
                                            patient_id=request.user.id, creator=request.user)

            print(request.POST.get("datum"), request.POST.get("tijd"), request.POST.get("glucose_value"))

    last_glucose_value = GlucoseValue.objects.all().filter(creator=request.user).order_by('datetime').last()
    initial_date = datetime.datetime.now().date()
    initial_time = datetime.datetime.now().time()
    if last_glucose_value:
        initial_date = last_glucose_value.datetime.date()
        initial_time = (last_glucose_value.datetime + datetime.timedelta(0,1800)).time()

    if request.GET and request.GET.get("select_date"):
        initial_date = datetime.datetime.strptime(request.GET.get("select_date"), '%Y-%m-%d').date()
    form = GlucoseValueForm(initial={"datum": initial_date, 'tijd': initial_time})

    glucose_values = GlucoseValue.objects.all().filter(creator=request.user).order_by('datetime')
    dates = glucose_values.order_by('datetime').values("datetime").distinct()
    glucose_values = glucose_values.filter(
        datetime__year=initial_date.year,
        datetime__month=initial_date.month,
        datetime__day=initial_date.day)

    date_list = []
    for date in dates:
        if date["datetime"].date() not in date_list:
            date_list.append(date["datetime"].date())

    return render(request, "upload_glucose.html", {'form': form, 'glucose_values': glucose_values,
                                                   "selected_date": initial_date, "date_list": date_list})