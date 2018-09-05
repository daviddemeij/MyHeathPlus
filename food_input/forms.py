from django import forms
from .models import FoodRecord, GlucoseValue, Measurement, User, Product
from dal import autocomplete
from datetimewidget.widgets import DateWidget, TimeWidget
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

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
        widget=TimeWidget(attrs={'id': "id_tijd", "autocomplete": "off"}, usel10n=False, bootstrap_version=3,
                          options={'format': 'hh:ii'})
    )

    class Meta:
        model = FoodRecord
        fields = ['patient_id', 'datum', 'tijd', 'missing_time', 'categorie', 'display_name', 'eenheid',
                  'koppel_eenheid_aan_alle_producten_binnen_deze_categorie', 'aantal_eenheden']
        widgets = {
            'display_name': autocomplete.ModelSelect2(url='product-autocomplete', forward=['categorie']),

        }
        labels = {'patient_id': _('Patient ID'),
                  'amount': _('Hoeveelheid (gram)'),
                  'display_name': _('Product'),
                  'missing_time': _('Tijd Onbekend')}


class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['name', 'amount', 'linked_product']


class GlucoseValueForm(forms.ModelForm):
    datum = forms.DateField(
        widget=DateWidget(attrs={'id': "id_datum", "autocomplete": "off"}, usel10n=True, bootstrap_version=3)
    )
    tijd = forms.TimeField(
        widget=TimeWidget(attrs={'id': "id_tijd", "autocomplete": "off"}, usel10n=False, bootstrap_version=3,
                          options={'format': 'hh:ii'})
    )

    class Meta:
        model = GlucoseValue
        fields = ['datum', 'tijd', 'glucose_value']
        widgets = {
            'glucose_value': forms.NumberInput(attrs={'step': "0.1"})
        }


class CopyMealForm(forms.Form):
    copy_date = forms.DateField(
        widget=DateWidget(attrs={'id': "copy_date", "autocomplete": "off"}, usel10n=True, bootstrap_version=3)
    )


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(label=_("Email address"), required=True,
                             help_text=_("Required."))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class SelectProductForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(),
                                     widget=autocomplete.ModelSelect2(url='product-id-autocomplete'))


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        delete = []
        for field_name, field in self.fields.items():
            if field:
                if field.label.startswith("Field"):
                    delete.append(field_name)
        for field_name in delete:
                del self.fields[field_name]
        self.fields['productgroep_oms'] = forms.ChoiceField(choices=CATEGORIES)
    #productgroep_oms = forms.ChoiceField(choices=CATEGORIES)
    class Meta:
        model = Product
        exclude = ("id", "occurrence", "is_nevo")
        widgets = {

        }
