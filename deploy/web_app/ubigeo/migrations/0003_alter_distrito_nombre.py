# Generated by Django 4.1.3 on 2022-11-29 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ubigeo', '0002_distrito_altitud_distrito_ubigeo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distrito',
            name='nombre',
            field=models.CharField(max_length=36),
        ),
    ]
