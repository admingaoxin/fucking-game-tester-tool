# Generated by Django 4.2.3 on 2023-09-16 08:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0003_alter_profile_head_img_headimage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="head_img",
            field=models.CharField(max_length=512, verbose_name="头像地址"),
        ),
    ]