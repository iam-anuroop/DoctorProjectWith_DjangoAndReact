# Generated by Django 4.2.5 on 2023-09-13 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_doctors_department_alter_doctors_hospital'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctors',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]