from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import FoodRecordSerializer, MeasurementSerializer, FoodRecordDetailSerializer, DisplayNameSerializer, \
    UserSerializer, FoodRecordUpdateSerializer
from .models import FoodRecord, Measurement, DisplayName, Product
from .actions import convert_int, calculate_nutrition
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings



@api_view(['GET', 'POST'])
def food_record_list(request):
    """
    List all food records, or create a food record.
    """
    if request.method == 'GET':
        food_records = FoodRecord.objects.filter(creator=request.user)
        serializer = FoodRecordSerializer(food_records, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = FoodRecordUpdateSerializer(data=data)
        if serializer.is_valid():
            instance = FoodRecord(**serializer.validated_data)
            instance.amount = float(instance.amount_of_measurements) * instance.measurement.amount
            instance.product = instance.display_name.product
            instance.patient_id = convert_int(request.user.get_username())
            instance.creator = request.user
            instance = calculate_nutrition(instance)
            existing_object = FoodRecord.objects.filter(patient_id=instance.patient_id).filter(
                datetime=instance.datetime).filter(product=instance.product).filter(amount=instance.amount).first()
            if existing_object:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                product = instance.product
                product.occurrence += 1
                product.save()
                instance.save()
                return Response(FoodRecordSerializer(instance).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def food_record(request, id):
    try:
        food_record = FoodRecord.objects.get(pk=id)
    except FoodRecord.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user != food_record.creator:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        serializer = FoodRecordDetailSerializer(food_record)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = FoodRecordUpdateSerializer(food_record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            food_record.amount = float(food_record.amount_of_measurements) * food_record.measurement.amount
            food_record.product = food_record.display_name.product
            food_record = calculate_nutrition(food_record)
            food_record.save()
            return Response(FoodRecordSerializer(food_record).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        product = food_record.product
        if product.occurrence > 0:
            product.occurrence -= 1
            product.save()
        food_record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def measurement_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        measurements = Measurement.objects.all()

        display_name = request.GET.get('display_name')
        if display_name:
            try:
                product = DisplayName.objects.get(pk=display_name).product
                measurements = measurements.filter(linked_product=product)
            except DisplayName.DoesNotExist:
                measurements = Measurement.objects.none()

        product = request.GET.get('product')
        if product:
            try:
                product = Product.objects.get(pk=product)
                measurements = measurements.filter(linked_product=product)
            except Product.DoesNotExist:
                measurements = Measurement.objects.none()


        query = request.GET.get('query')
        if query:
            for s in query.split(" "):
                measurements = measurements.filter(name__icontains=s) | measurements.filter(amount__icontains=s)

        serializer = MeasurementSerializer(measurements, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def product_list(request):
    if request.method == 'GET':
        products = DisplayName.objects.all()

        category = request.GET.get('category')
        if category and category != "<geen categorie>":
            products = products.filter(product__productgroep_oms=category)

        query = request.GET.get('query')
        if query:
            for s in query.split(" "):
                products = products.filter(name__icontains=s) | products.filter(product__fabrikantnaam__icontains=s)

        products = products.order_by('-product__occurrence')
        serializer = DisplayNameSerializer(products, many=True)
        return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid() and serializer.validated_data['username']:
            if convert_int(serializer.validated_data['username']):
                user = User(
                    username=serializer.validated_data['username']
                )
                user.set_password(serializer.validated_data['password'])
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                user.save()

                return JsonResponse({"token": token})
            else:
                return JsonResponse({"username": ["Please use an integer as userneme"]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
