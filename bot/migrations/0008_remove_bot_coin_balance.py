# Generated by Django 3.2.8 on 2022-01-12 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0007_auto_20220110_1752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bot',
            name='coin_balance',
        ),
    ]