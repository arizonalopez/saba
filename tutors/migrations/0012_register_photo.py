# Generated by Django 3.1.3 on 2021-10-26 18:06

from django.db import migrations, models
import tutors.models


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0011_auto_20211026_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='photo',
            field=models.ImageField(null=True, upload_to=tutors.models.upload_to, verbose_name='Photo'),
        ),
    ]