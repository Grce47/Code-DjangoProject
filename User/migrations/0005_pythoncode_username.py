# Generated by Django 4.0.4 on 2022-05-25 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0004_pythoncode_session_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='pythoncode',
            name='username',
            field=models.TextField(null=True),
        ),
    ]
