# Generated by Django 4.1.4 on 2022-12-13 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
