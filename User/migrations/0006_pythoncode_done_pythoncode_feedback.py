# Generated by Django 4.0.4 on 2022-05-28 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0005_pythoncode_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='pythoncode',
            name='done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pythoncode',
            name='feedback',
            field=models.TextField(null=True),
        ),
    ]
