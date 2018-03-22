from django.shortcuts import render, redirect
from .forms import FoodRecordForm
from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, FoodRecord, Measurement
from django.views.generic import ListView

import datetime
# Create your views here.
@login_required
def home(request):
    if request.method == 'POST':
        form = FoodRecordForm(request.POST)
        if form.is_valid():
            eenheid = Measurement.objects.get(pk=request.POST.get("eenheid"))
            instance = form.save(commit=False)  # does nothing, just trigger the validation
            instance.amount = float(request.POST.get("aantal_eenheden")) * eenheid.amount

            if instance.product not in eenheid.linked_product.all():
                eenheid.linked_product.add(instance.product)
            instance.creator = request.user
            fields = [field.name for field in FoodRecord._meta.fields + FoodRecord._meta.many_to_many]

            for field in fields:
                if field.startswith("field_"):
                    nutrition_value = getattr(instance.product, field)
                    if nutrition_value:
                        if "sp" in nutrition_value:
                            nutrition_value = 0.0
                        setattr(instance, field, float(nutrition_value)*(instance.amount / float(instance.product.hoeveelheid)))
            instance.save()
        else:
            print("input is not valid!")
    else:
        form = FoodRecordForm()
    food_records = FoodRecord.objects.filter(creator=request.user).order_by('-created_at')
    return render(request, 'home.html', {'form': form, 'food_records': food_records})

@login_required
def delete_record(request, id):
    record = FoodRecord.objects.filter(pk=id).first()
    if record:
        if record.creator == request.user:
            record.delete()
    return redirect('/')


class ProductAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated():
        #    return Product.objects.none()

        if not self.request.user.is_authenticated:
            return Product.objects.none()

        qs = Product.objects.all()

        category = self.forwarded.get('category', None)

        if category and category != "<geen categorie>":
            qs = qs.filter(productgroep_oms=category)

        if self.q:
            qs = qs.filter(product_omschrijving__icontains=self.q)

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

