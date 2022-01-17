# Generated by Django 3.2.8 on 2022-01-10 01:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trade', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('balance', models.FloatField(max_length=100)),
                ('market', models.CharField(max_length=200)),
                ('coin_balance', models.FloatField(max_length=100)),
                ('volume', models.FloatField(max_length=100)),
                ('is_bid', models.BooleanField()),
                ('status', models.BooleanField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField()),
                ('side', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('volume', models.FloatField(max_length=100)),
                ('price', models.FloatField(max_length=100)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade.bot')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
