# Generated by Django 3.2.7 on 2022-05-19 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='epoch_time_micro',
            field=models.BigIntegerField(default=1652921019375293),
        ),
        migrations.AlterField(
            model_name='order',
            name='epoch_time_micro',
            field=models.BigIntegerField(default=1652921019376293),
        ),
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.PositiveBigIntegerField(),
        ),
        migrations.AlterField(
            model_name='stockhiddenattribute',
            name='epoch_time_micro',
            field=models.BigIntegerField(default=1652921019376293),
        ),
    ]
