# Generated by Django 3.2.6 on 2023-04-17 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apigw', '0021_auto_20230414_0900'),
    ]

    operations = [
        migrations.AddField(
            model_name='apiservicelog',
            name='parameters_urlappendGET',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
