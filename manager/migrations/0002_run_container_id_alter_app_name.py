# Generated by Django 4.1.3 on 2022-11-22 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='run',
            name='container_id',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='app',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
