# Generated by Django 2.2.5 on 2020-04-21 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='information',
            name='filename',
            field=models.CharField(default='filename_default', max_length=100),
            preserve_default=False,
        ),
    ]