# Generated by Django 3.0.5 on 2024-01-03 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shared.helper


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0172_auto_20231130_0823'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['-created_date'], 'verbose_name': 'Genre', 'verbose_name_plural': 'Genres'},
        ),
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ['-created_date'], 'verbose_name': 'Movie', 'verbose_name_plural': 'Movies'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['-created_date'], 'verbose_name': 'Tag', 'verbose_name_plural': 'Tags'},
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
            field=models.FileField(blank=True, null=True, upload_to=shared.helper.Helper.get_file_path, verbose_name='cover'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='cover_credit',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='cover_credit'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='featured'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='hidden',
            field=models.BooleanField(default=False, verbose_name='hidden'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='order',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='order'),
        ),
        migrations.AlterField(
            model_name='media',
            name='cover',
            field=models.FileField(blank=True, null=True, upload_to=shared.helper.Helper.get_file_path),
        ),
        migrations.AlterField(
            model_name='movie',
            name='cover',
            field=models.FileField(blank=True, null=True, upload_to=shared.helper.Helper.get_file_path, verbose_name='cover'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='_description'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='director',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='director'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='director_link',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='director_link'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='duration',
            field=models.FloatField(default=0, verbose_name='duration'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='embed',
            field=models.TextField(blank=True, default='', null=True, verbose_name='embed'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(blank=True, to='content.Genre', verbose_name='_genre'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='height',
            field=models.FloatField(default=0, verbose_name='height'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='hidden',
            field=models.BooleanField(default=False, verbose_name='hidden'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to=shared.helper.Helper.get_file_path, verbose_name='media'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='prizes',
            field=models.TextField(blank=True, null=True, verbose_name='prizes'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='rating',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='rating'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='tag',
            field=models.ManyToManyField(blank=True, to='content.Tag', verbose_name='_tag'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='triggers',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='triggers'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='views',
            field=models.IntegerField(default=0, verbose_name='views'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='width',
            field=models.FloatField(default=0, verbose_name='width'),
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
            field=models.FileField(blank=True, null=True, upload_to=shared.helper.Helper.get_file_path, verbose_name='cover'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='custom_letter',
            field=models.BooleanField(default=False, verbose_name='custom_letter'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='genre',
            field=models.BooleanField(default=False, verbose_name='genre'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='hidden',
            field=models.BooleanField(default=False, verbose_name='hidden'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='order',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='order'),
        ),
        migrations.CreateModel(
            name='WatchParty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=36, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('movie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.Movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='MessageWatchParty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('watch_party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.WatchParty')),
            ],
            options={
                'ordering': ['created_date'],
            },
        ),
    ]
