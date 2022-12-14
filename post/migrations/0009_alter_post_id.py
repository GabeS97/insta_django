# Generated by Django 4.1.4 on 2022-12-14 04:08

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_alter_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.UUIDField(default=uuid.UUID('b5d754a9-282f-481f-9363-f9dcc732092b'), editable=False, primary_key=True, serialize=False),
        ),
    ]