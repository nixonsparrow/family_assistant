# Generated by Django 3.0.5 on 2021-11-03 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_auto_20211103_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
