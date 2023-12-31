# Generated by Django 3.2.7 on 2022-05-18 22:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default='', max_length=1000)),
                ('shares_outstanding', models.BigIntegerField(default=300000000)),
                ('symbol', models.CharField(max_length=5, unique=True)),
                ('quote', models.FloatField(default=None, null=True)),
                ('active', models.BooleanField(default=False)),
                ('epoch_time_micro', models.BigIntegerField(default=1652911643903570)),
            ],
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incoming_order_id', models.BigIntegerField()),
                ('book_order_id', models.BigIntegerField()),
                ('symbol', models.CharField(max_length=5)),
                ('instruction', models.CharField(choices=[('BUY', 'BUY'), ('SELL', 'SELL')], max_length=5)),
                ('quantity', models.BigIntegerField()),
                ('price', models.FloatField()),
                ('timestamp', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserSecuritiesAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('C', 'CASH')], default='C', max_length=1)),
                ('cash_balance', models.FloatField(default=0.0)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('trading_level', models.PositiveSmallIntegerField(choices=[(1, 'No Experience'), (2, 'Beginner'), (3, 'Intermediate'), (4, 'Advanced'), (5, 'Professional')], null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StockHiddenAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rand_norm_mean', models.FloatField(default=0.0)),
                ('rand_norm_std', models.FloatField(default=1.0)),
                ('market_cap', models.BigIntegerField(default=None, null=True)),
                ('epoch_time_micro', models.BigIntegerField(default=1652911643903570)),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.company')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=5)),
                ('order_type', models.CharField(choices=[('MKT', 'MARKET'), ('LMT', 'LIMIT'), ('CNL', 'CANCEL')], max_length=5)),
                ('instruction', models.CharField(choices=[('BUY', 'BUY'), ('SELL', 'SELL')], max_length=5)),
                ('quantity', models.BigIntegerField()),
                ('price', models.FloatField(null=True)),
                ('remainder', models.BigIntegerField()),
                ('status', models.CharField(default='PENDING', max_length=100)),
                ('epoch_time_micro', models.BigIntegerField(default=1652911643904570)),
                ('user_securities_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.usersecuritiesaccount')),
            ],
        ),
        migrations.CreateModel(
            name='Equity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=5)),
                ('quantity', models.BigIntegerField(default=0)),
                ('basis', models.FloatField(default=0.0)),
                ('user_securities_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.usersecuritiesaccount')),
            ],
        ),
    ]
