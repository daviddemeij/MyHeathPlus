from django.conf.urls import url
from django.urls import path
from . import views
urlpatterns = [path('', views.home),
               url('product-autocomplete/',
               views.ProductAutocomplete.as_view(),
               name='product-autocomplete'),
               path('<int:id>/', views.delete_record, name="delete_record")]
