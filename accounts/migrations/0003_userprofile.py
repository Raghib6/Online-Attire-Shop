# Generated by Django 3.2.4 on 2021-09-05 13:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_useraccount_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line1', models.CharField(blank=True, max_length=150, null=True)),
                ('address_line2', models.CharField(blank=True, max_length=150, null=True)),
                ('profile_pic', models.ImageField(blank=True, upload_to='profile_pic')),
                ('region', models.CharField(blank=True, max_length=50)),
                ('country', models.CharField(blank=True, default='Bangladesh', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]