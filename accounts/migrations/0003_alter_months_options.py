# Generated by Django 3.2.3 on 2022-03-08 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_months_month_index'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='months',
            options={'ordering': ['month_index'], 'verbose_name': 'Month', 'verbose_name_plural': 'Months'},
        ),
    ]