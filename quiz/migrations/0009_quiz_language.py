# Generated by Django 3.1.2 on 2020-10-12 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_auto_20200922_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='language',
            field=models.CharField(choices=[('ES', 'Español'), ('EN', 'English')], default='ES', max_length=2),
            preserve_default=False,
        ),
    ]
