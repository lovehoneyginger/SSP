# Generated by Django 4.0.5 on 2022-07-16 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentLogin', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enrolledclass',
            name='enrolled_course_name',
        ),
    ]
