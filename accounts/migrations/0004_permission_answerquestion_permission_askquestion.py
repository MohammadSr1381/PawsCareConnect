# Generated by Django 4.2.7 on 2024-02-01 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_permission_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='answerQuestion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='permission',
            name='askQuestion',
            field=models.BooleanField(default=False),
        ),
    ]