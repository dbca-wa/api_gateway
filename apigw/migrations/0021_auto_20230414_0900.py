# Generated by Django 3.2.6 on 2023-04-14 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apigw', '0020_auto_20230414_0857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apiservice',
            name='oauth2_api_url',
        ),
        migrations.AlterField(
            model_name='apiservice',
            name='service_type',
            field=models.IntegerField(choices=[(1, 'AWS (AWSRequestsAuth)'), (2, 'HTTP/s Request (GET)'), (3, 'HTTP/s Request (POST)'), (4, 'OAuth2 Bearer (GET)')], default=0),
        ),
    ]
