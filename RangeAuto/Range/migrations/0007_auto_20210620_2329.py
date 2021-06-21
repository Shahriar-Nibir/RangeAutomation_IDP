# Generated by Django 3.2.3 on 2021-06-20 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Range', '0006_auto_20210620_2302'),
    ]

    operations = [
        migrations.AddField(
            model_name='fire',
            name='detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Range.detail'),
        ),
        migrations.AddField(
            model_name='fire',
            name='new_target',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
