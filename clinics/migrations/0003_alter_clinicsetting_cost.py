# Generated by Django 4.2.7 on 2024-01-29 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0002_alter_clinicsetting_closing_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicsetting',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=20000, max_digits=10),
        ),
    ]