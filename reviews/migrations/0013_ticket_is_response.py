# Generated by Django 5.1.2 on 2024-10-25 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0012_remove_review_review_id_alter_review_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='is_response',
            field=models.BooleanField(default=False),
        ),
    ]