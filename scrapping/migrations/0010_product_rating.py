# Generated by Django 3.0.6 on 2020-05-15 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapping', '0009_auto_20200515_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]