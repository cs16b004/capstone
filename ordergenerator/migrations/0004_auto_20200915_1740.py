# Generated by Django 3.1.1 on 2020-09-15 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordergenerator', '0003_order_traded_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(default='Waiting', editable=False, max_length=10),
        ),
    ]
