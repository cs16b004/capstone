# Generated by Django 3.1.1 on 2020-09-18 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordergenerator', '0006_order_trade_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user_MinFill',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='order',
            name='user_all',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='order',
            name='user_disclosed',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
