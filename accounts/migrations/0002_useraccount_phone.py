# Generated by Django 3.2.4 on 2021-08-28 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='phone',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
