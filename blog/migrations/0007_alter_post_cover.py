# Generated by Django 4.1.7 on 2023-06-04 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_alter_post_cover"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="cover",
            field=models.ImageField(default="default-avatar.png", upload_to="covers/"),
        ),
    ]
