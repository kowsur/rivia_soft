# Generated by Django 3.1.7 on 2021-05-01 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0008_auto_20210501_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='selfassesment',
            name='selfassesment_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='selfassesment_type_id', to='companies.selfassesmenttype', verbose_name='Selfassesment Type'),
        ),
    ]