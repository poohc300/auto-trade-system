# Generated by Django 3.2.8 on 2022-01-10 01:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0002_auto_20220110_1030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactionhistory',
            name='bot',
        ),
        migrations.DeleteModel(
            name='Bot',
        ),
        migrations.DeleteModel(
            name='TransactionHistory',
        ),
    ]
