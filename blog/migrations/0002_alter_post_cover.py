# Generated by Django 4.1.7 on 2023-06-03 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="cover",
            field=models.ImageField(default="default.png", upload_to='covers/%Y%m%d"'),
        ),
    ]