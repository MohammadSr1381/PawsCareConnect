# Generated by Django 4.2.7 on 2024-01-30 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_alter_appointment_clinic_alter_appointment_patient_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentslot',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
