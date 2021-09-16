# Generated by Django 3.2.4 on 2021-09-16 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_userprofile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='address_line1',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address_line2',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(blank=True, default='Bangladesh', max_length=150),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='region',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
