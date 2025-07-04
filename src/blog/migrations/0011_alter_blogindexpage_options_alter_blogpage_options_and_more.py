# Generated by Django 5.2.3 on 2025-06-15 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_remove_navbarlink_sort_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogindexpage',
            options={'verbose_name': 'Blog home page', 'verbose_name_plural': 'Blog home pages'},
        ),
        migrations.AlterModelOptions(
            name='blogpage',
            options={'verbose_name': 'Blog post', 'verbose_name_plural': 'Blog posts'},
        ),
        migrations.AlterModelOptions(
            name='blogtagindexpage',
            options={'verbose_name': 'Blog tag posts page', 'verbose_name_plural': 'Blog tag posts pages'},
        ),
        migrations.AddField(
            model_name='author',
            name='abstract',
            field=models.CharField(blank=True, max_length=255, verbose_name='small abstract'),
        ),
    ]
