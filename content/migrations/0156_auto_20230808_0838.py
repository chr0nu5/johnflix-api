# Generated by Django 3.0.5 on 2023-08-08 11:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shared.helper


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0155_auto_20230125_2007'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.DeleteModel(
            name='Ache',
        ),
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
        migrations.AddField(
            model_name='watchlist',
            name='episode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.Episode'),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='movie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.Movie'),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
