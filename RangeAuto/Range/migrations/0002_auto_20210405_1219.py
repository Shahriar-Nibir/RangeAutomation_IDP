# Generated by Django 3.1.2 on 2021-04-05 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Range', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firer',
            name='number',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
