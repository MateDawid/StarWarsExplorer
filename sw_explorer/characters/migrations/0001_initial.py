# Generated by Django 4.1.6 on 2023-02-11 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.BinaryField()),
                ('filename', models.CharField(max_length=128)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]