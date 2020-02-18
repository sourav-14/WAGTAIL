# Generated by Django 3.0.3 on 2020-02-17 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(help_text='Email Address', max_length=100)),
                ('full_name', models.CharField(help_text='First and Last Name', max_length=100)),
            ],
        ),
    ]
