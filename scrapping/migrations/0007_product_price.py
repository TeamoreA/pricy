# Generated by Django 3.0.6 on 2020-05-15 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapping', '0006_auto_20200515_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
