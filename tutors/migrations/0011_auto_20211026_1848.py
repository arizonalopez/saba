# Generated by Django 3.1.3 on 2021-10-26 17:48

from django.db import migrations, models
import tutors.validator


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0010_importantdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Price ($)'),
        ),
        migrations.AlterField(
            model_name='register',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, validators=[tutors.validator.validate_name], verbose_name='Name'),
        ),
    ]
