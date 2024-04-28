# Generated by Django 3.0.5 on 2022-11-10 15:05

from django.db import migrations, models
import shared.helper


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0096_auto_20221110_0257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='cover',
            field=models.FileField(blank=True, null=True, upload_to=shared.helper.Helper.get_file_path),
        ),
        migrations.AlterField(
            model_name='episode',
            name='cover',
            field=models.FileField(blank=True, null=True, upload_to=shared.helper.Helper.get_file_path),
        ),
        migrations.AlterField(
            model_name='episode',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to=shared.helper.Helper.get_file_path),
        ),
        migrations.AlterField(
            model_name='genre',
            name='cover',
            field=models.FileField(blank=True, null=True, upload_to=shared.helper.Helper.get_file_path),
        ),
        migrations.AlterField(
            model_name='media',
            name='cover',
            field=models.FileField(blank=True, null=True, upload_to=shared.helper.Helper.get_file_path),
        ),
        migrations.AlterField(
            model_name='movie',
            name='cover',
            field=models.FileField(blank=True, null=True, upload_to=shared.helper.Helper.get_file_path),
        ),
        migrations.AlterField(
            model_name='movie',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to=shared.helper.Helper.get_file_path),
        ),
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.FileField(upload_to=shared.helper.Helper.get_file_path),
        ),
        migrations.AlterField(
            model_name='photocollection',
            name='cover',
            field=models.FileField(blank=True, null=True, upload_to=shared.helper.Helper.get_file_path),
        ),
        migrations.AlterField(
            model_name='subtitle',
            name='vtt',
            field=models.FileField(upload_to=shared.helper.Helper.get_file_path),
        ),
        migrations.AlterField(
            model_name='tag',
            name='cover',
            field=models.FileField(blank=True, null=True, upload_to=shared.helper.Helper.get_file_path),
        ),
    ]
