# Generated by Django 3.2.3 on 2021-06-20 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Range', '0007_auto_20210620_2329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='detect',
        ),
        migrations.RemoveField(
            model_name='result',
            name='fired',
        ),
        migrations.RemoveField(
            model_name='result',
            name='hits',
        ),
        migrations.AddField(
            model_name='result',
            name='fire',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Range.fire'),
        ),
    ]
