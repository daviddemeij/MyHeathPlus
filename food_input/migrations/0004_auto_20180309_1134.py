# Generated by Django 2.0.3 on 2018-03-09 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food_input', '0003_auto_20180309_1127'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='foodrecord',
            unique_together={('patient_id', 'datetime', 'product')},
        ),
    ]
