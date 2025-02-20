# Generated by Django 5.1.4 on 2025-01-11 14:38

import Accounts.managers
import Accounts.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ID',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(max_length=15, unique=True)),
                ('patient_type', models.CharField(choices=[('', '-----'), ('Member_Patient', 'Member_Patient'), ('NextOfKin_Patient', 'NextOfKin_Patient'), ('Staff', 'Staff'), ('New_Patient', 'New_Patient')], max_length=50)),
                ('registered', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Patient ID',
                'verbose_name_plural': 'Patient IDs',
            },
        ),
        migrations.CreateModel(
            name='NextOfKin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kin_first_name', models.CharField(max_length=50)),
                ('kin_code', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('kin_last_name', models.CharField(max_length=50)),
                ('relationship', models.CharField(choices=[('', '----------'), ('Brother', 'Brother'), ('Sister', 'Sister'), ('Son', 'Son'), ('Daughter', 'Daughter'), ('Mother', 'Mother'), ('Father', 'Father'), ('Aunt', 'Aunt'), ('Uncle', 'Uncle'), ('Niece', 'Niece'), ('Nephew', 'Nephew'), ('Cousin', 'Cousin'), ('Other close Relative', 'Other close Relative'), ('Wife', 'Wife'), ('Husband', 'Husband'), ('Guardian', 'Guardian')], max_length=50)),
                ('kin_mobile_number', models.CharField(blank=True, max_length=13, null=True)),
            ],
            options={
                'verbose_name': 'Next of Kin',
                'verbose_name_plural': 'Next of Kins',
            },
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp_code', models.CharField(max_length=6)),
                ('otp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('otp_verified', models.BooleanField(default=False)),
                ('for_email', models.EmailField(blank=True, default='', max_length=254, null=True)),
            ],
            options={
                'verbose_name': 'OTP',
                'verbose_name_plural': 'OTPs',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_Member_Patient', models.BooleanField(default=False)),
                ('has_next_of_kin', models.BooleanField(default=False)),
                ('is_Doctor', models.BooleanField(default=False)),
                ('specialization', models.CharField(blank=True, choices=[('', '----------'), ('Dentistry', 'Dentistry'), ('Pharmacy', 'Pharmacy'), ('Consultation', 'Consultation'), ('Laboratory', 'Laboratory Tests'), ('Other issue', 'Other issue')], max_length=19)),
                ('profile_photo', models.ImageField(default='icon/bondijunction_dentalclinic_logo-300x258.jpg', upload_to='profile_photos/')),
                ('patient_type', models.CharField(choices=[('', '-----'), ('Member_Patient', 'Member_Patient'), ('NextOfKin_Patient', 'NextOfKin_Patient'), ('Staff', 'Staff'), ('New_Patient', 'New_Patient')], max_length=50, null=True)),
                ('patient_id', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('member_code', models.CharField(default=Accounts.models.generate_service_id, max_length=6, unique=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='', max_length=10)),
                ('mobile_number', models.CharField(blank=True, max_length=13, null=True, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('next_of_kin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Accounts.nextofkin')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', Accounts.managers.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='nextofkin',
            name='related_patient',
            field=models.ForeignKey(limit_choices_to=models.Q(('is_Member_Patient', True), ('mobile_number', True), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Related Patient'),
        ),
    ]
