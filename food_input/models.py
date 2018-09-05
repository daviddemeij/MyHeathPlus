from django.db import models
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
import datetime as dt

class Product(models.Model):
    id = models.IntegerField(blank=True, null=False, primary_key=True)
    occurrence = models.IntegerField(blank=False, null=False, default=0)
    productgroep_oms = models.TextField(db_column='Productgroep_oms', blank=True, null=True)  # Field name made lowercase.
    productgroepcode = models.TextField(db_column='Productgroepcode', blank=True, null=True)  # Field name made lowercase.
    controlegetal = models.TextField(db_column='Controlegetal', blank=True, null=True)  # Field name made lowercase.
    product_omschrijving = models.TextField(db_column='Product_omschrijving', blank=True, null=True)  # Field name made lowercase.
    product_description = models.TextField(db_column='Product_description', blank=True, null=True)  # Field name made lowercase.
    fabrikantnaam = models.TextField(db_column='Fabrikantnaam', blank=True, null=True)  # Field name made lowercase.
    code_nonactief = models.TextField(db_column='Code_nonactief', blank=True, null=True)  # Field name made lowercase.
    hoeveelheid = models.TextField(db_column='Hoeveelheid', blank=True, null=True)  # Field name made lowercase.
    meeteenheid = models.TextField(db_column='Meeteenheid', blank=True, null=True)  # Field name made lowercase.
    eetbaar_gedeelte = models.TextField(db_column='Eetbaar_gedeelte', blank=True, null=True)  # Field name made lowercase.
    vertrouwelijk_code = models.TextField(db_column='Vertrouwelijk_code', blank=True, null=True)  # Field name made lowercase.
    commentaarregel = models.TextField(db_column='Commentaarregel', blank=True, null=True)  # Field name made lowercase.
    field_01001 = models.TextField(db_column='_01001', blank=True, null=True, verbose_name="Energy (kcal)")
    field_01002 = models.TextField(db_column='_01002', blank=True, null=True, verbose_name="Energy (kJ)")
    field_02001 = models.TextField(db_column='_02001', blank=True, null=True, verbose_name="Nitrogen total (g)")
    field_02002 = models.TextField(db_column='_02002', blank=True, null=True, verbose_name="Protein total (g)")
    field_02003 = models.TextField(db_column='_02003', blank=True, null=True, verbose_name="Protein vegetable (g)")
    field_02004 = models.TextField(db_column='_02004', blank=True, null=True, verbose_name="Protein animal (g)")
    field_03001 = models.TextField(db_column='_03001', blank=True, null=True, verbose_name="Fat total (g)")
    field_03002 = models.TextField(db_column='_03002', blank=True, null=True, verbose_name="Fatty acids total (g)")
    field_03004 = models.TextField(db_column='_03004', blank=True, null=True, verbose_name="Fatty acids saturated (g)")
    field_03006 = models.TextField(db_column='_03006', blank=True, null=True, verbose_name="Fatty acids mono unsaturated cis (g)")
    field_03008 = models.TextField(db_column='_03008', blank=True, null=True, verbose_name="Fatty acids poly unsaturated (g)")
    field_03009 = models.TextField(db_column='_03009', blank=True, null=True)
    field_03010 = models.TextField(db_column='_03010', blank=True, null=True)
    field_03011 = models.TextField(db_column='_03011', blank=True, null=True)
    field_03012 = models.TextField(db_column='_03012', blank=True, null=True)
    field_03013 = models.TextField(db_column='_03013', blank=True, null=True)
    field_03014 = models.TextField(db_column='_03014', blank=True, null=True)
    field_03015 = models.TextField(db_column='_03015', blank=True, null=True)
    field_03016 = models.TextField(db_column='_03016', blank=True, null=True)
    field_03017 = models.TextField(db_column='_03017', blank=True, null=True)
    field_03018 = models.TextField(db_column='_03018', blank=True, null=True)
    field_03019 = models.TextField(db_column='_03019', blank=True, null=True)
    field_03020 = models.TextField(db_column='_03020', blank=True, null=True)
    field_03021 = models.TextField(db_column='_03021', blank=True, null=True)
    field_03022 = models.TextField(db_column='_03022', blank=True, null=True)
    field_03023 = models.TextField(db_column='_03023', blank=True, null=True)
    field_03024 = models.TextField(db_column='_03024', blank=True, null=True)
    field_03025 = models.TextField(db_column='_03025', blank=True, null=True)
    field_03026 = models.TextField(db_column='_03026', blank=True, null=True)
    field_03027 = models.TextField(db_column='_03027', blank=True, null=True)
    field_03028 = models.TextField(db_column='_03028', blank=True, null=True)
    field_03029 = models.TextField(db_column='_03029', blank=True, null=True)
    field_03030 = models.TextField(db_column='_03030', blank=True, null=True)
    field_03031 = models.TextField(db_column='_03031', blank=True, null=True)
    field_03033 = models.TextField(db_column='_03033', blank=True, null=True)
    field_03034 = models.TextField(db_column='_03034', blank=True, null=True)
    field_03035 = models.TextField(db_column='_03035', blank=True, null=True)
    field_03036 = models.TextField(db_column='_03036', blank=True, null=True)
    field_03037 = models.TextField(db_column='_03037', blank=True, null=True)
    field_03038 = models.TextField(db_column='_03038', blank=True, null=True)
    field_03039 = models.TextField(db_column='_03039', blank=True, null=True)
    field_03040 = models.TextField(db_column='_03040', blank=True, null=True)
    field_03041 = models.TextField(db_column='_03041', blank=True, null=True)
    field_03042 = models.TextField(db_column='_03042', blank=True, null=True)
    field_03043 = models.TextField(db_column='_03043', blank=True, null=True)
    field_03044 = models.TextField(db_column='_03044', blank=True, null=True)
    field_03045 = models.TextField(db_column='_03045', blank=True, null=True)
    field_03046 = models.TextField(db_column='_03046', blank=True, null=True)
    field_03047 = models.TextField(db_column='_03047', blank=True, null=True)
    field_03048 = models.TextField(db_column='_03048', blank=True, null=True)
    field_03049 = models.TextField(db_column='_03049', blank=True, null=True)
    field_03052 = models.TextField(db_column='_03052', blank=True, null=True)
    field_03053 = models.TextField(db_column='_03053', blank=True, null=True)
    field_03054 = models.TextField(db_column='_03054', blank=True, null=True)
    field_03055 = models.TextField(db_column='_03055', blank=True, null=True)
    field_03057 = models.TextField(db_column='_03057', blank=True, null=True)
    field_03058 = models.TextField(db_column='_03058', blank=True, null=True)
    field_03059 = models.TextField(db_column='_03059', blank=True, null=True)
    field_03060 = models.TextField(db_column='_03060', blank=True, null=True)
    field_03061 = models.TextField(db_column='_03061', blank=True, null=True)
    field_03062 = models.TextField(db_column='_03062', blank=True, null=True)
    field_03065 = models.TextField(db_column='_03065', blank=True, null=True)
    field_03089 = models.TextField(db_column='_03089', blank=True, null=True)
    field_03090 = models.TextField(db_column='_03090', blank=True, null=True)
    field_03103 = models.TextField(db_column='_03103', blank=True, null=True)
    field_03104 = models.TextField(db_column='_03104', blank=True, null=True)
    field_03105 = models.TextField(db_column='_03105', blank=True, null=True)
    field_03106 = models.TextField(db_column='_03106', blank=True, null=True)
    field_03107 = models.TextField(db_column='_03107', blank=True, null=True)
    field_03108 = models.TextField(db_column='_03108', blank=True, null=True)
    field_03109 = models.TextField(db_column='_03109', blank=True, null=True)
    field_03113 = models.TextField(db_column='_03113', blank=True, null=True)
    field_03114 = models.TextField(db_column='_03114', blank=True, null=True)
    field_03115 = models.TextField(db_column='_03115', blank=True, null=True)
    field_03116 = models.TextField(db_column='_03116', blank=True, null=True)
    field_03131 = models.TextField(db_column='_03131', blank=True, null=True)
    field_03133 = models.TextField(db_column='_03133', blank=True, null=True)
    field_03134 = models.TextField(db_column='_03134', blank=True, null=True)
    field_03135 = models.TextField(db_column='_03135', blank=True, null=True)
    field_03136 = models.TextField(db_column='_03136', blank=True, null=True, verbose_name="Fatty acids trans (g)")
    field_03138 = models.TextField(db_column='_03138', blank=True, null=True)
    field_03139 = models.TextField(db_column='_03139', blank=True, null=True)
    field_03140 = models.TextField(db_column='_03140', blank=True, null=True)
    field_03141 = models.TextField(db_column='_03141', blank=True, null=True)
    field_03142 = models.TextField(db_column='_03142', blank=True, null=True)
    field_04001 = models.TextField(db_column='_04001', blank=True, null=True, verbose_name="Cholesterol (mg)")
    field_05001 = models.TextField(db_column='_05001', blank=True, null=True, verbose_name="Carbohydrates total (g)")
    field_05002 = models.TextField(db_column='_05002', blank=True, null=True, verbose_name="Sugar (g)")
    field_05010 = models.TextField(db_column='_05010', blank=True, null=True)
    field_05011 = models.TextField(db_column='_05011', blank=True, null=True)
    field_06001 = models.TextField(db_column='_06001', blank=True, null=True, verbose_name="Fiber total (g)")
    field_07001 = models.TextField(db_column='_07001', blank=True, null=True, verbose_name="Water (g)")
    field_08001 = models.TextField(db_column='_08001', blank=True, null=True, verbose_name="Alcohol total (g)")
    field_09001 = models.TextField(db_column='_09001', blank=True, null=True, verbose_name="Calcium (mg)")
    field_09002 = models.TextField(db_column='_09002', blank=True, null=True, verbose_name="Phosphorus (mg)")
    field_09003 = models.TextField(db_column='_09003', blank=True, null=True, verbose_name="Iron total (mg)")
    field_09004 = models.TextField(db_column='_09004', blank=True, null=True)
    field_09005 = models.TextField(db_column='_09005', blank=True, null=True)
    field_09006 = models.TextField(db_column='_09006', blank=True, null=True, verbose_name="Natrium (mg)")
    field_09007 = models.TextField(db_column='_09007', blank=True, null=True, verbose_name="Potassium (mg)")
    field_09008 = models.TextField(db_column='_09008', blank=True, null=True, verbose_name="Magnesium (mg)")
    field_09009 = models.TextField(db_column='_09009', blank=True, null=True, verbose_name="Zinc (mg)")
    field_10001 = models.TextField(db_column='_10001', blank=True, null=True, verbose_name="Selenium (ug)")
    field_10002 = models.TextField(db_column='_10002', blank=True, null=True, verbose_name="Copper (mg)")
    field_10003 = models.TextField(db_column='_10003', blank=True, null=True, verbose_name="Iodine (ug)")
    field_11001 = models.TextField(db_column='_11001', blank=True, null=True, verbose_name="Retinol (ug)")
    field_11002 = models.TextField(db_column='_11002', blank=True, null=True, verbose_name="Retinol equivalents (ug)")
    field_11003 = models.TextField(db_column='_11003', blank=True, null=True, verbose_name="Beta-carotene (ug)")
    field_11005 = models.TextField(db_column='_11005', blank=True, null=True, verbose_name="Vitamin B1 (mg)")
    field_11006 = models.TextField(db_column='_11006', blank=True, null=True, verbose_name="Vitamin B2 (mg)")
    field_11007 = models.TextField(db_column='_11007', blank=True, null=True, verbose_name="Vitamin B6 (mg)")
    field_11008 = models.TextField(db_column='_11008', blank=True, null=True, verbose_name="Vitamin B12 (ug)")
    field_11009 = models.TextField(db_column='_11009', blank=True, null=True, verbose_name="Vitamin D total (ug)")
    field_11010 = models.TextField(db_column='_11010', blank=True, null=True, verbose_name="Vitamin E total (ug)")
    field_11011 = models.TextField(db_column='_11011', blank=True, null=True, verbose_name="Vitamin C total (mg)")
    field_11012 = models.TextField(db_column='_11012', blank=True, null=True)
    field_11013 = models.TextField(db_column='_11013', blank=True, null=True)
    field_11014 = models.TextField(db_column='_11014', blank=True, null=True)
    field_11015 = models.TextField(db_column='_11015', blank=True, null=True)
    field_11016 = models.TextField(db_column='_11016', blank=True, null=True)
    field_11017 = models.TextField(db_column='_11017', blank=True, null=True)
    field_11018 = models.TextField(db_column='_11018', blank=True, null=True)
    field_11019 = models.TextField(db_column='_11019', blank=True, null=True)
    field_11020 = models.TextField(db_column='_11020', blank=True, null=True)
    field_11021 = models.TextField(db_column='_11021', blank=True, null=True)
    field_11022 = models.TextField(db_column='_11022', blank=True, null=True)
    field_11023 = models.TextField(db_column='_11023', blank=True, null=True)
    field_11024 = models.TextField(db_column='_11024', blank=True, null=True)
    field_11027 = models.TextField(db_column='_11027', blank=True, null=True)
    field_11028 = models.TextField(db_column='_11028', blank=True, null=True)
    field_11035 = models.TextField(db_column='_11035', blank=True, null=True, verbose_name="Vitamin K total (ug)")
    field_11036 = models.TextField(db_column='_11036', blank=True, null=True)
    field_11038 = models.TextField(db_column='_11038', blank=True, null=True)
    field_11046 = models.TextField(db_column='_11046', blank=True, null=True)
    field_12001 = models.TextField(db_column='_12001', blank=True, null=True)
    field_13006 = models.TextField(db_column='_13006', blank=True, null=True)
    is_nevo = models.BooleanField(default=True, blank=False, null=False)

    def __str__(self):
        if self.fabrikantnaam != "":
            return self.fabrikantnaam + " " + self.product_omschrijving + " (" + self.productgroep_oms + ")"
        else:
            return self.product_omschrijving + " (" + self.productgroep_oms + ")"

    class Meta:
        managed = True
        db_table = 'food_input_product'


class Measurement(models.Model):
    linked_product = models.ManyToManyField(Product, blank=True)
    name = models.TextField()
    amount = models.FloatField()
    created_at = models.DateTimeField(default=dt.datetime.now)
    def __str__(self):
        return str(self.name) + " (" + str(self.amount) + " gram)"

class DisplayName(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    name = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=dt.datetime.now)

    def __str__(self):
        if self.product.fabrikantnaam != "":
            return self.product.fabrikantnaam + " " + self.name + " (" + self.product.productgroep_oms + ")"
        else:
            return self.name + " (" + self.product.productgroep_oms + ")"

# Create your models here.
class FoodRecord(models.Model):
    patient_id = models.IntegerField()
    datetime = models.DateTimeField()
    missing_time = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    display_name = models.ForeignKey(DisplayName, on_delete=models.PROTECT, blank=True, null=True)
    amount = models.FloatField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    created_at = models.DateTimeField(default=dt.datetime.now)
    measurement = models.ForeignKey(Measurement, on_delete=models.PROTECT, null=True, blank=True)
    amount_of_measurements = models.FloatField(null=True, blank=True)

    field_01001 = models.TextField(db_column='_01001', blank=True, null=True)
    field_01002 = models.TextField(db_column='_01002', blank=True, null=True)
    field_02001 = models.TextField(db_column='_02001', blank=True, null=True)
    field_02002 = models.TextField(db_column='_02002', blank=True, null=True)
    field_02003 = models.TextField(db_column='_02003', blank=True, null=True)
    field_02004 = models.TextField(db_column='_02004', blank=True, null=True)
    field_03001 = models.TextField(db_column='_03001', blank=True, null=True)
    field_03002 = models.TextField(db_column='_03002', blank=True, null=True)
    field_03004 = models.TextField(db_column='_03004', blank=True, null=True)
    field_03006 = models.TextField(db_column='_03006', blank=True, null=True)
    field_03008 = models.TextField(db_column='_03008', blank=True, null=True)
    field_03009 = models.TextField(db_column='_03009', blank=True, null=True)
    field_03010 = models.TextField(db_column='_03010', blank=True, null=True)
    field_03011 = models.TextField(db_column='_03011', blank=True, null=True)
    field_03012 = models.TextField(db_column='_03012', blank=True, null=True)
    field_03013 = models.TextField(db_column='_03013', blank=True, null=True)
    field_03014 = models.TextField(db_column='_03014', blank=True, null=True)
    field_03015 = models.TextField(db_column='_03015', blank=True, null=True)
    field_03016 = models.TextField(db_column='_03016', blank=True, null=True)
    field_03017 = models.TextField(db_column='_03017', blank=True, null=True)
    field_03018 = models.TextField(db_column='_03018', blank=True, null=True)
    field_03019 = models.TextField(db_column='_03019', blank=True, null=True)
    field_03020 = models.TextField(db_column='_03020', blank=True, null=True)
    field_03021 = models.TextField(db_column='_03021', blank=True, null=True)
    field_03022 = models.TextField(db_column='_03022', blank=True, null=True)
    field_03023 = models.TextField(db_column='_03023', blank=True, null=True)
    field_03024 = models.TextField(db_column='_03024', blank=True, null=True)
    field_03025 = models.TextField(db_column='_03025', blank=True, null=True)
    field_03026 = models.TextField(db_column='_03026', blank=True, null=True)
    field_03027 = models.TextField(db_column='_03027', blank=True, null=True)
    field_03028 = models.TextField(db_column='_03028', blank=True, null=True)
    field_03029 = models.TextField(db_column='_03029', blank=True, null=True)
    field_03030 = models.TextField(db_column='_03030', blank=True, null=True)
    field_03031 = models.TextField(db_column='_03031', blank=True, null=True)
    field_03033 = models.TextField(db_column='_03033', blank=True, null=True)
    field_03034 = models.TextField(db_column='_03034', blank=True, null=True)
    field_03035 = models.TextField(db_column='_03035', blank=True, null=True)
    field_03036 = models.TextField(db_column='_03036', blank=True, null=True)
    field_03037 = models.TextField(db_column='_03037', blank=True, null=True)
    field_03038 = models.TextField(db_column='_03038', blank=True, null=True)
    field_03039 = models.TextField(db_column='_03039', blank=True, null=True)
    field_03040 = models.TextField(db_column='_03040', blank=True, null=True)
    field_03041 = models.TextField(db_column='_03041', blank=True, null=True)
    field_03042 = models.TextField(db_column='_03042', blank=True, null=True)
    field_03043 = models.TextField(db_column='_03043', blank=True, null=True)
    field_03044 = models.TextField(db_column='_03044', blank=True, null=True)
    field_03045 = models.TextField(db_column='_03045', blank=True, null=True)
    field_03046 = models.TextField(db_column='_03046', blank=True, null=True)
    field_03047 = models.TextField(db_column='_03047', blank=True, null=True)
    field_03048 = models.TextField(db_column='_03048', blank=True, null=True)
    field_03049 = models.TextField(db_column='_03049', blank=True, null=True)
    field_03052 = models.TextField(db_column='_03052', blank=True, null=True)
    field_03053 = models.TextField(db_column='_03053', blank=True, null=True)
    field_03054 = models.TextField(db_column='_03054', blank=True, null=True)
    field_03055 = models.TextField(db_column='_03055', blank=True, null=True)
    field_03057 = models.TextField(db_column='_03057', blank=True, null=True)
    field_03058 = models.TextField(db_column='_03058', blank=True, null=True)
    field_03059 = models.TextField(db_column='_03059', blank=True, null=True)
    field_03060 = models.TextField(db_column='_03060', blank=True, null=True)
    field_03061 = models.TextField(db_column='_03061', blank=True, null=True)
    field_03062 = models.TextField(db_column='_03062', blank=True, null=True)
    field_03065 = models.TextField(db_column='_03065', blank=True, null=True)
    field_03089 = models.TextField(db_column='_03089', blank=True, null=True)
    field_03090 = models.TextField(db_column='_03090', blank=True, null=True)
    field_03103 = models.TextField(db_column='_03103', blank=True, null=True)
    field_03104 = models.TextField(db_column='_03104', blank=True, null=True)
    field_03105 = models.TextField(db_column='_03105', blank=True, null=True)
    field_03106 = models.TextField(db_column='_03106', blank=True, null=True)
    field_03107 = models.TextField(db_column='_03107', blank=True, null=True)
    field_03108 = models.TextField(db_column='_03108', blank=True, null=True)
    field_03109 = models.TextField(db_column='_03109', blank=True, null=True)
    field_03113 = models.TextField(db_column='_03113', blank=True, null=True)
    field_03114 = models.TextField(db_column='_03114', blank=True, null=True)
    field_03115 = models.TextField(db_column='_03115', blank=True, null=True)
    field_03116 = models.TextField(db_column='_03116', blank=True, null=True)
    field_03131 = models.TextField(db_column='_03131', blank=True, null=True)
    field_03133 = models.TextField(db_column='_03133', blank=True, null=True)
    field_03134 = models.TextField(db_column='_03134', blank=True, null=True)
    field_03135 = models.TextField(db_column='_03135', blank=True, null=True)
    field_03136 = models.TextField(db_column='_03136', blank=True, null=True)
    field_03138 = models.TextField(db_column='_03138', blank=True, null=True)
    field_03139 = models.TextField(db_column='_03139', blank=True, null=True)
    field_03140 = models.TextField(db_column='_03140', blank=True, null=True)
    field_03141 = models.TextField(db_column='_03141', blank=True, null=True)
    field_03142 = models.TextField(db_column='_03142', blank=True, null=True)
    field_04001 = models.TextField(db_column='_04001', blank=True, null=True)
    field_05001 = models.TextField(db_column='_05001', blank=True, null=True)
    field_05002 = models.TextField(db_column='_05002', blank=True, null=True)
    field_05010 = models.TextField(db_column='_05010', blank=True, null=True)
    field_05011 = models.TextField(db_column='_05011', blank=True, null=True)
    field_06001 = models.TextField(db_column='_06001', blank=True, null=True)
    field_07001 = models.TextField(db_column='_07001', blank=True, null=True)
    field_08001 = models.TextField(db_column='_08001', blank=True, null=True)
    field_09001 = models.TextField(db_column='_09001', blank=True, null=True)
    field_09002 = models.TextField(db_column='_09002', blank=True, null=True)
    field_09003 = models.TextField(db_column='_09003', blank=True, null=True)
    field_09004 = models.TextField(db_column='_09004', blank=True, null=True)
    field_09005 = models.TextField(db_column='_09005', blank=True, null=True)
    field_09006 = models.TextField(db_column='_09006', blank=True, null=True)
    field_09007 = models.TextField(db_column='_09007', blank=True, null=True)
    field_09008 = models.TextField(db_column='_09008', blank=True, null=True)
    field_09009 = models.TextField(db_column='_09009', blank=True, null=True)
    field_10001 = models.TextField(db_column='_10001', blank=True, null=True)
    field_10002 = models.TextField(db_column='_10002', blank=True, null=True)
    field_10003 = models.TextField(db_column='_10003', blank=True, null=True)
    field_11001 = models.TextField(db_column='_11001', blank=True, null=True)
    field_11002 = models.TextField(db_column='_11002', blank=True, null=True)
    field_11003 = models.TextField(db_column='_11003', blank=True, null=True)
    field_11005 = models.TextField(db_column='_11005', blank=True, null=True)
    field_11006 = models.TextField(db_column='_11006', blank=True, null=True)
    field_11007 = models.TextField(db_column='_11007', blank=True, null=True)
    field_11008 = models.TextField(db_column='_11008', blank=True, null=True)
    field_11009 = models.TextField(db_column='_11009', blank=True, null=True)
    field_11010 = models.TextField(db_column='_11010', blank=True, null=True)
    field_11011 = models.TextField(db_column='_11011', blank=True, null=True)
    field_11012 = models.TextField(db_column='_11012', blank=True, null=True)
    field_11013 = models.TextField(db_column='_11013', blank=True, null=True)
    field_11014 = models.TextField(db_column='_11014', blank=True, null=True)
    field_11015 = models.TextField(db_column='_11015', blank=True, null=True)
    field_11016 = models.TextField(db_column='_11016', blank=True, null=True)
    field_11017 = models.TextField(db_column='_11017', blank=True, null=True)
    field_11018 = models.TextField(db_column='_11018', blank=True, null=True)
    field_11019 = models.TextField(db_column='_11019', blank=True, null=True)
    field_11020 = models.TextField(db_column='_11020', blank=True, null=True)
    field_11021 = models.TextField(db_column='_11021', blank=True, null=True)
    field_11022 = models.TextField(db_column='_11022', blank=True, null=True)
    field_11023 = models.TextField(db_column='_11023', blank=True, null=True)
    field_11024 = models.TextField(db_column='_11024', blank=True, null=True)
    field_11027 = models.TextField(db_column='_11027', blank=True, null=True)
    field_11028 = models.TextField(db_column='_11028', blank=True, null=True)
    field_11035 = models.TextField(db_column='_11035', blank=True, null=True)
    field_11036 = models.TextField(db_column='_11036', blank=True, null=True)
    field_11038 = models.TextField(db_column='_11038', blank=True, null=True)
    field_11046 = models.TextField(db_column='_11046', blank=True, null=True)
    field_12001 = models.TextField(db_column='_12001', blank=True, null=True)
    field_13006 = models.TextField(db_column='_13006', blank=True, null=True)

    class Meta:
        unique_together = ('patient_id', 'datetime', 'product', 'amount')

    def __str__(self):
        return " Patient " + str(self.patient_id) + " (" + self.datetime.strftime('%Y-%m-%d %H:%M') + ") - " + self.product.product_omschrijving + " (" + str(self.amount) + " gram) "

class GlucoseValue(models.Model):
    id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField(null=False, blank=False)
    patient_id = models.IntegerField(null=False, blank=False)
    glucose_value = models.FloatField(null=False, blank=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=dt.datetime.now)

    class Meta:
        unique_together = ('datetime', 'patient_id')