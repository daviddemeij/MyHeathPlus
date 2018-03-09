from django import forms
from .models import FoodRecord, Product
from dal import autocomplete
from datetimewidget.widgets import DateTimeWidget

CATEGORIES = (("", "<geen categorie>"),
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
    class Meta:
        model = FoodRecord
        fields = ['patient_id', 'datetime', 'amount', 'category', 'product']
        widgets = {
            'product': autocomplete.ModelSelect2(url='product-autocomplete', forward=['category']),
            'datetime': DateTimeWidget(attrs={'id': "id_datetime"}, usel10n=True, bootstrap_version=3)
        }