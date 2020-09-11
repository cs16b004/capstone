# Generated by Django 3.1.1 on 2020-09-10 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordergenerator', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='No_extra',
        ),
        migrations.AddField(
            model_name='order',
            name='user_id',
            field=models.CharField(default='YAUID', max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_price',
            field=models.FloatField(default=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_quantity',
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.CharField(choices=[('LM', 'Limit'), ('MR', 'Market')], default='MR', max_length=10),
        ),
    ]