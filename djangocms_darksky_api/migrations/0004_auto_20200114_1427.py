# Generated by Django 2.2.9 on 2020-01-14 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_darksky_api', '0003_auto_20200113_1036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='darkskyapi',
            name='template_size',
        ),
        migrations.AddField(
            model_name='darkskyapi',
            name='template',
            field=models.CharField(choices=[('light', 'Light'), ('full', 'Full')], default='light', max_length=2, verbose_name='Template'),
        ),
    ]
