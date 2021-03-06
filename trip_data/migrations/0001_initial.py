# Generated by Django 3.2.12 on 2022-04-20 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='trip_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('address', models.TextField(blank=True)),
                ('transport', models.TextField(blank=True)),
                ('mrt', models.TextField(blank=True)),
                ('latitude', models.TextField(blank=True)),
                ('longitude', models.TextField(blank=True)),
                ('stitle', models.TextField(blank=True)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'trip_data',
            },
        ),
    ]
