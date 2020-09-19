# Generated by Django 3.0.7 on 2020-06-05 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('cinema_code', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('city', models.CharField(default='تهران', max_length=30)),
                ('capacity', models.IntegerField()),
                ('phone_number', models.CharField(max_length=20, null=True)),
                ('address', models.TextField()),
            ],
        ),
    ]