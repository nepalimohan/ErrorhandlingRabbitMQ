# Generated by Django 5.0.6 on 2024-07-07 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField()),
                ('total_quantity', models.IntegerField()),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]