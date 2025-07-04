# Generated by Django 5.2.3 on 2025-06-15 11:57

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_bloghomepage_bloglistpage_and_more'),
        ('wagtailcore', '0094_alter_page_locale'),
    ]

    operations = [
        migrations.AddField(
            model_name='navbarlink',
            name='page',
            field=modelcluster.fields.ParentalKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.page', verbose_name='page'),
        ),
        migrations.AlterField(
            model_name='navbarlink',
            name='link',
            field=models.URLField(blank=True, verbose_name='link'),
        ),
    ]
