# Generated by Django 4.0.4 on 2022-08-18 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='weight',
            field=models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1, help_text='权重高展示顺序靠前', verbose_name='权重'),
        ),
        migrations.AlterField(
            model_name='link',
            name='href',
            field=models.URLField(verbose_name='链接'),
        ),
    ]
