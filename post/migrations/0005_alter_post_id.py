# Generated by Django 4.1.4 on 2022-12-13 21:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_alter_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.UUIDField(default=uuid.UUID('ce880543-0463-4f85-a8dc-5735abd124e6'), editable=False, primary_key=True, serialize=False),
        ),
    ]