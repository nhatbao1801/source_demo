# Generated by Django 3.2.6 on 2022-04-16 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20220416_0223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refaccount',
            name='id',
            field=models.TextField(default='72c509e270934c44aed6d86d905ba645', primary_key=True, serialize=False),
        ),
    ]
