# Generated by Django 3.1 on 2020-08-29 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0004_auto_20200420_2019"),
    ]

    operations = [
        migrations.AddField(
            model_name="quiz",
            name="status",
            field=models.CharField(
                choices=[("DF", "Draft"), ("PB", "Published")],
                default="DF",
                max_length=2,
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="quiz",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions",
                to="quiz.quiz",
            ),
        ),
        migrations.AlterField(
            model_name="quiz",
            name="slug",
            field=models.SlugField(max_length=150, unique=True),
        ),
    ]
