# Generated by Django 3.2.3 on 2022-03-06 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0041_auto_20220306_1820'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseSources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Expense Source',
                'verbose_name_plural': 'Expense Sources',
            },
        ),
        migrations.CreateModel(
            name='IncomeSources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Income Source',
                'verbose_name_plural': 'Income Sources',
            },
        ),
        migrations.CreateModel(
            name='Months',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_name', models.CharField(max_length=10, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Month',
                'verbose_name_plural': 'Months',
            },
        ),
        migrations.CreateModel(
            name='IncomesPerTaxYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('comission', models.IntegerField(default=0)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='companies.selfassesment')),
                ('income_source', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='accounts.incomesources')),
                ('month', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='accounts.months')),
                ('tax_year', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='companies.selfassesmentaccountsubmissiontaxyear')),
            ],
            options={
                'verbose_name': 'Income Per Tax Year',
                'verbose_name_plural': 'Incomes Per Tax Year',
            },
        ),
        migrations.CreateModel(
            name='ExpensesPerTaxYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='companies.selfassesment')),
                ('expense_source', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='accounts.incomesources')),
                ('month', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='accounts.months')),
                ('tax_year', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='companies.selfassesmentaccountsubmissiontaxyear')),
            ],
            options={
                'verbose_name': 'Expense Per Tax Year',
                'verbose_name_plural': 'Expenses Per Tax Year',
            },
        ),
    ]