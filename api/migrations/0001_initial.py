# Generated by Django 5.2.3 on 2025-06-23 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('sku', models.CharField(max_length=100, unique=True)),
                ('lote', models.CharField(max_length=100)),
                ('codigo_barras', models.CharField(max_length=255, unique=True)),
            ],
        ),
    ]
