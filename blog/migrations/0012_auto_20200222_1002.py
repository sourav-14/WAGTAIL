# Generated by Django 3.0.3 on 2020-02-22 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20200222_0901'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogdetailpage',
            name='tags',
        ),
        migrations.DeleteModel(
            name='BlogPageTag',
        ),
    ]