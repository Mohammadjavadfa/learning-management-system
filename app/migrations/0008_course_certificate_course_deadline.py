# Generated by Django 5.0.3 on 2024-03-09 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_language_course_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='certificate',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='deadline',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
