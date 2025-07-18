# Generated by Django 5.2.3 on 2025-07-04 14:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='shop_app.category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('description', models.TextField(max_length=1500)),
                ('tax_rate', models.DecimalField(decimal_places=2, default=23.0, help_text='Stawka VAT w % (np. 23.00, 8.00, 0.00)', max_digits=4)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='shop_app.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products_gallery')),
                ('alt_text', models.CharField(blank=True, max_length=255)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop_app.product')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ProductSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nazwa specyfikacji')),
                ('value', models.CharField(max_length=255, verbose_name='Wartość')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='shop_app.product')),
            ],
            options={
                'verbose_name': 'Specyfikacja produktu',
                'verbose_name_plural': 'Specyfikacje produktu',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_name', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('sku', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='shop_app.product')),
            ],
            options={
                'ordering': ['price'],
            },
        ),
        migrations.CreateModel(
            name='ProductVariantSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nazwa specyfikacji')),
                ('value', models.CharField(max_length=255, verbose_name='Wartość')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='shop_app.productvariant')),
            ],
            options={
                'verbose_name': 'Specyfikacja wariantu',
                'verbose_name_plural': 'Specyfikacje wariantu',
                'ordering': ['name'],
            },
        ),
    ]
