# Generated by Django 4.1.7 on 2023-06-04 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0009_alter_post_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="cover",
            field=models.ImageField(
                default="default-avatar.png", upload_to="covers%Y%m%d"
            ),
        ),
    ]
