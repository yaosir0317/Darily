# Generated by Django 2.1.2 on 2018-11-20 08:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0010_auto_20181120_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classstudyrecord',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='讲师'),
        ),
    ]
