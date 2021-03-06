from django.conf.urls import url, include
from django.urls import path
from . import views
from . import api
from .actions import count_occurrence
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
print("Counting occurrence!")
count_occurrence()

urlpatterns = [path('', views.home),
               url('product-autocomplete/', views.ProductAutocomplete.as_view(), name='product-autocomplete'),
               url('measurement-autocomplete/', views.MeasurementAutocomplete.as_view(), name='measurement-autocomplete'),
               url('product-id-autocomplete/', views.ProductIdAutocomplete.as_view(), name='product-id-autocomplete'),
               path('<int:id>/', views.delete_record, name="delete_record"),
               path('count/', views.count),
               url('api/login/', obtain_jwt_token),
               url('api/register/', api.register),
               url('api/refresh-token/', refresh_jwt_token),
               path('api/food_records/<int:id>/', api.food_record, name="food_record"),
               url('api/food_records/', api.food_record_list),
               url('api/measurements/', api.measurement_list),
               url('api/products/', api.product_list),
               url('display_names/', views.update_display_names, name="display_names")
               ]
