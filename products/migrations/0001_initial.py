# Generated by Django 3.2.4 on 2021-06-06 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=50, unique=True)),
                ('cat_slug', models.SlugField(max_length=150, unique=True)),
                ('cat_image', models.ImageField(blank=True, upload_to='categories')),
                ('cat_created', models.DateTimeField(auto_now_add=True)),
                ('cat_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='products.category')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=150)),
                ('product_slug', models.SlugField(max_length=200, unique=True)),
                ('product_desc', models.TextField(blank=True)),
                ('product_price', models.IntegerField()),
                ('product_image', models.ImageField(upload_to='products')),
                ('product_stock', models.IntegerField()),
                ('is_available', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('product_cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
        ),
    ]
