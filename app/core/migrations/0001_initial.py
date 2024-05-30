# Generated by Django 5.0.6 on 2024-05-30 18:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('con_id', models.CharField(max_length=16, verbose_name='Contract Id')),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name_plural': 'Contracts',
                'unique_together': {('con_id', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.CharField(max_length=64)),
                ('con_id', models.CharField(max_length=16, verbose_name='Contract Id')),
                ('parent_id', models.CharField(blank=True, max_length=16, null=True)),
                ('order_id', models.CharField(max_length=16)),
                ('order_ref', models.CharField(blank=True, max_length=16, null=True)),
                ('order_description', models.CharField(blank=True, max_length=128, null=True)),
                ('last_execution_time', models.DateTimeField()),
                ('side', models.CharField(max_length=4)),
                ('order_type', models.CharField(max_length=16)),
                ('status', models.CharField(max_length=16)),
                ('total_size', models.FloatField(null=True)),
                ('price', models.FloatField(null=True)),
                ('avg_price', models.FloatField(null=True)),
                ('stop_price', models.FloatField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Orders',
                'unique_together': {('account_id', 'order_id')},
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('con_id', models.CharField(db_index=True, max_length=16, verbose_name='Contract Id')),
                ('update_time', models.DateTimeField()),
                ('last', models.FloatField()),
                ('bid', models.FloatField()),
                ('ask', models.FloatField()),
            ],
            options={
                'verbose_name_plural': 'Prices',
                'unique_together': {('con_id', 'update_time')},
            },
        ),
        migrations.CreateModel(
            name='Strategy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('side', models.CharField(choices=[('BUY', 'Buy'), ('SELL', 'Sell')], default='BUY', max_length=4)),
                ('account_id', models.CharField(max_length=16)),
                ('quantity', models.FloatField()),
                ('limit_percentage', models.FloatField()),
                ('stop_percentage', models.FloatField()),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.contract')),
            ],
            options={
                'verbose_name_plural': 'Strategies',
                'unique_together': {('name', 'contract')},
            },
        ),
    ]
