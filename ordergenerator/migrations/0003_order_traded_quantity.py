# Generated by Django 3.1.1 on 2020-09-15 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordergenerator', '0002_auto_20200910_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='traded_quantity',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
