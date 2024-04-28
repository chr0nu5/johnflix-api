# Generated by Django 3.0.5 on 2023-09-05 18:21

from django.db import migrations, models
import shared.helper


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0160_auto_20230822_1153'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['-created_date'], 'verbose_name': 'Lista', 'verbose_name_plural': 'Listas'},
        ),
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ['-created_date'], 'verbose_name': 'Filme', 'verbose_name_plural': 'Filmes'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['-created_date'], 'verbose_name': 'Etiqueta', 'verbose_name_plural': 'Etiquetas'},
        ),
        migrations.RemoveField(
            model_name='tag',
            name='featured',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='searchable',
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
            field=models.FileField(blank=True, null=True, upload_to=shared.helper.Helper.get_file_path, verbose_name='Capa'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='cover_credit',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Crédito da imagem'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Caso está lista vá aparecer como destaque, adicione aqui um texto de descrição'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='Este item é um destaque'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='hidden',
            field=models.BooleanField(default=False, verbose_name='Ocultar'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='order',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Posição'),
        ),
        migrations.AlterField(
            model_name='media',
            name='cover',
            field=models.FileField(blank=True, null=True, upload_to=shared.helper.Helper.get_file_path),
        ),
        migrations.AlterField(
            model_name='movie',
            name='cover',
            field=models.FileField(blank=True, null=True, upload_to=shared.helper.Helper.get_file_path, verbose_name='Capa'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='Data de lançamento do filme'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Sinopse do filme'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='director',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome da pessoa diretora'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='director_link',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Página web da pessoa diretora'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='duration',
            field=models.FloatField(default=0, verbose_name='Duração do filme (em minutos)'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='embed',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Insira aqui o código de embed (Youtube ou Vimeo)'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='frames',
            field=models.FloatField(default=0, verbose_name='frames'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(blank=True, to='content.Genre', verbose_name='Esta etiqueta é um genero'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='height',
            field=models.FloatField(default=0, verbose_name='Altura'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='hidden',
            field=models.BooleanField(default=False, verbose_name='Ocultar'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to=shared.helper.Helper.get_file_path, verbose_name='Arquivo'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='prizes',
            field=models.TextField(blank=True, null=True, verbose_name='Prêmios que este filme já ganhou'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='rating',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Classificação indicativa'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='tag',
            field=models.ManyToManyField(blank=True, to='content.Tag', verbose_name='Etiqueta'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Título'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='triggers',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Gatilhos'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='views',
            field=models.IntegerField(default=0, verbose_name='Visualizações'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='width',
            field=models.FloatField(default=0, verbose_name='Largura'),
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
            field=models.FileField(blank=True, null=True, upload_to=shared.helper.Helper.get_file_path, verbose_name='Capa'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='custom_letter',
            field=models.BooleanField(default=False, verbose_name='Esta etiqueta é uma letra'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='genre',
            field=models.BooleanField(default=False, verbose_name='Esta etiqueta é um genero'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='hidden',
            field=models.BooleanField(default=False, verbose_name='Ocultar'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='order',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Posição'),
        ),
    ]
