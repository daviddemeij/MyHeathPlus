from django import forms
from .models import FoodRecord, Product, Measurement
from dal import autocomplete
from datetimewidget.widgets import DateTimeWidget
from django.utils.translation import ugettext_lazy as _

CATEGORIES = (("<geen categorie>", "<geen categorie>"),
              ("Aardappelen", "Aardappelen"),
              ("Graanproducten en bindmiddelen", "Graanproducten en bindmiddelen"),
              ("Groenten", "Groenten"),
              ("Fruit", "Fruit"),
              ("Preparaten", "Preparaten"),
              ("Eieren", "Eieren"),
              ("Vlees, vleeswaren en gevogelte", "Vlees, vleeswaren en gevogelte"),
              ("Vis", "Vis"),
              ("Peulvruchten", "Peulvruchten"),
              ("Noten, zaden en snacks", "Noten, zaden en snacks"),
              ("Kruiden en specerijen", "Kruiden en specerijen"),
              ("Diversen", "Diversen"),
              ("Brood", "Brood"),
              ("Gebak en koek", "Gebak en koek"),
              ("Melk en melkproducten", "Melk en melkproducten"),
              ("Kaas", "Kaas"),
              ("Vetten, oliën en hartige sauzen", "Vetten, oliën en hartige sauzen"),
              ("Samengestelde gerechten", "Samengestelde gerechten"),
              ("Suiker, snoep, zoet beleg en zoete sauzen", "Suiker, snoep, zoet beleg en zoete sauzen"),
              ("Alcoholische en niet-alcoholische dranken", "Alcoholische en niet-alcoholische dranken"),
              ("Hartig broodbeleg", "Hartig broodbeleg"),
              ("Sojaproducten en vegetarische producten", "Sojaproducten en vegetarische producten"),
              ("Soepen", "Soepen")
              )

class FoodRecordForm(forms.ModelForm):
    category = forms.ChoiceField(choices=CATEGORIES)
    eenheid = forms.ModelChoiceField(
        queryset=Measurement.objects.all().order_by('amount'),
        widget=autocomplete.ModelSelect2(url='measurement-autocomplete', forward=['product'])
    )
    aantal_eenheden = forms.FloatField()
    class Meta:
        model = FoodRecord
        fields = ['patient_id', 'datetime', 'category', 'product', 'eenheid', 'aantal_eenheden']
        widgets = {
            'product': autocomplete.ModelSelect2(url='product-autocomplete', forward=['category']),
            'datetime': DateTimeWidget(attrs={'id': "id_datetime"}, usel10n=True, bootstrap_version=3)
        }
        labels = {'patient_id': _('Patient ID'),
                  'datetime': _('Datum & tijd'),
                  'amount': _('Hoeveelheid (gram)'),
                  'product': _('Product')}

class MeasurementForm(forms.ModelForm):
    category = forms.ChoiceField(choices=CATEGORIES)

    class Meta:
        model = Measurement
        fields = ['category', 'linked_product', 'name', 'amount']
        widgets = {
            'linked_product': autocomplete.ModelSelect2Multiple(url='product-autocomplete', forward=['category'])
        }