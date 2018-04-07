from django.conf.urls import url
from django.urls import path
from . import views
from .actions import count_occurrence
print("Counting occurrence!")
count_occurrence()

urlpatterns = [path('', views.home),
               url('product-autocomplete/',
               views.ProductAutocomplete.as_view(),
               name='product-autocomplete'),
                url('measurement-autocomplete/',
               views.MeasurementAutocomplete.as_view(),
               name='measurement-autocomplete'),
               path('<int:id>/', views.delete_record, name="delete_record"),
               path('count/', views.count)]
