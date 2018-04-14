from rest_framework import serializers
from .models import FoodRecord, Measurement, DisplayName
from django.contrib.auth.models import User

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        exclude = ('linked_product', 'created_at')

class DisplayNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisplayName
        fields = ('id', 'name')

class FoodRecordSerializer(serializers.ModelSerializer):
    measurement = MeasurementSerializer()
    display_name = DisplayNameSerializer()

    class Meta:
        model = FoodRecord
        fields = ('id', 'datetime', 'display_name', 'measurement', 'amount_of_measurements', 'amount', 'field_01001',
                  'field_05001', 'field_02002', 'field_03001', 'patient_id')


class FoodRecordUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodRecord
        fields = ('datetime', 'display_name', 'measurement', 'amount_of_measurements')


class FoodRecordDetailSerializer(serializers.ModelSerializer):
    measurement = MeasurementSerializer(read_only=True)
    display_name = DisplayNameSerializer(read_only=True)

    class Meta:
        model = FoodRecord
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



