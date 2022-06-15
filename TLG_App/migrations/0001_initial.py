# Generated by Django 4.0.4 on 2022-06-15 01:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Athlete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(choices=[('Freshman', 'Freshman'), ('Sophomore', 'Sophomore'), ('Junior', 'Junior'), ('Senior', 'Senior')], max_length=9)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('weight', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1400)])),
                ('dob', models.DateField(max_length=8)),
                ('weightclass', models.CharField(default=None, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='LiftHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lift', models.CharField(max_length=255)),
                ('weight', models.IntegerField()),
                ('date_of_lift', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='MaxLift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('image', models.ImageField(upload_to=None)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=255)),
                ('primary_color', models.CharField(max_length=255)),
                ('secondary_color', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
            ],
        ),
    ]
