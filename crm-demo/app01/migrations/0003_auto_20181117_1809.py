# Generated by Django 2.1.2 on 2018-11-17 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20181117_1759'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='permission',
            options={'verbose_name': '权限表', 'verbose_name_plural': '权限表'},
        ),
    ]
