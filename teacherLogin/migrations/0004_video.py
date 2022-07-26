# Generated by Django 4.0.5 on 2022-07-20 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacherLogin', '0003_alter_pdf_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='VIDEO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True, unique=True)),
                ('video', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('video_class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacherLogin.class')),
            ],
        ),
    ]
