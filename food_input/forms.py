from django import forms
from .models import FoodRecord, Product, Measurement
from dal import autocomplete
from datetimewidget.widgets import DateWidget, TimeWidget
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
    categorie = forms.ChoiceField(choices=CATEGORIES)
    eenheid = forms.ModelChoiceField(
        queryset=Measurement.objects.all().order_by('amount'),
        widget=autocomplete.ModelSelect2(url='measurement-autocomplete', forward=['display_name'])
    )
    koppel_eenheid_aan_alle_producten_binnen_deze_categorie = forms.BooleanField(required=False)
    aantal_eenheden = forms.FloatField()
    datum = forms.DateField(
        widget=DateWidget(attrs={'id': "id_datum", "autocomplete": "off"}, usel10n=True, bootstrap_version=3)
    )
    tijd = forms.TimeField(
        widget=TimeWidget(attrs={'id': "id_tijd", "autocomplete": "off"}, usel10n=False, bootstrap_version=3, options={'format': 'hh:ii'})
    )
    class Meta:
        model = FoodRecord
        fields = ['patient_id', 'datum', 'tijd', 'categorie', 'display_name', 'eenheid', 'koppel_eenheid_aan_alle_producten_binnen_deze_categorie', 'aantal_eenheden']
        widgets = {
            'display_name': autocomplete.ModelSelect2(url='product-autocomplete', forward=['categorie']),

        }
        labels = {'patient_id': _('Patient ID'),
                  'amount': _('Hoeveelheid (gram)'),
                  'display_name': _('Product')}

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['name', 'amount', 'linked_product']