# Generated by Django 3.2.6 on 2022-04-16 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_alter_event_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, help_text='Mô tả về sự kiện', null=True),
        ),
    ]
