# Generated by Django 5.1.4 on 2025-01-11 14:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Clinic', '0001_initial'),
        ('Dashboard', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_number', models.IntegerField(default=0, null='TRUE')),
                ('fullname', models.CharField(max_length=250)),
                ('mobile_number', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=100)),
                ('date_of_appointment', models.CharField(max_length=250)),
                ('time_of_appointment', models.CharField(max_length=250)),
                ('additional_msg', models.TextField(blank=True)),
                ('remark', models.CharField(default=0, max_length=250)),
                ('status', models.CharField(default=0, max_length=200)),
                ('prescription', models.TextField(blank=True, default=0)),
                ('recommended_test', models.TextField(blank=True, default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('appoint_status', models.CharField(choices=[('', '-----'), ('Failed', 'Failed'), ('Scheduled', 'Scheduled'), ('Canceled', 'Canceled'), ('Completed', 'Completed')], max_length=10, null=True, verbose_name='Status')),
                ('payment', models.BooleanField(blank=True, choices=[(True, 'Verified'), (False, 'N/A')], default=False, null=True, verbose_name='Payment')),
                ('appointee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patients', to=settings.AUTH_USER_MODEL)),
                ('doctor_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Dashboard.doctorreg')),
                ('worry_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Clinic.specialization')),
            ],
        ),
    ]
