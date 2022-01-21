# Generated by Django 3.2.8 on 2022-01-10 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='coin_balance',
            field=models.FloatField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='bot',
            name='is_bid',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='bot',
            name='market',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='bot',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='bot',
            name='volume',
            field=models.FloatField(blank=True, max_length=100),
        ),
    ]