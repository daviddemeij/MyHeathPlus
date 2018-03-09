from django.shortcuts import render
from .forms import FoodRecordForm
from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, FoodRecord
from django.views.generic import ListView

import datetime
# Create your views here.
@login_required
def home(request):
    food_records = FoodRecord.objects.filter(creator=request.user).order_by('-created_at')
    if request.method == 'POST':
        form = FoodRecordForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)  # does nothing, just trigger the validation
            instance.creator = request.user
            instance.save()
        else:
            print("input is not valid!")
    else:
        form = FoodRecordForm()
    return render(request, 'home.html', {'form': form, 'food_records': food_records })


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
            qs = qs.filter(product_omschrijving__contains=self.q)

        return qs
