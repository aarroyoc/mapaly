# Generated by Django 3.1 on 2020-09-17 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20200829_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='front_image',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]