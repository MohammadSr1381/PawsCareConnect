# Generated by Django 4.2.7 on 2024-01-26 17:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
        ('clinics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient_user', to=settings.AUTH_USER_MODEL)),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient_profile', to='accounts.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('is_activated', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to='patients.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('answer_text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answered_questions', to='clinics.clinic')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asked_questions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
