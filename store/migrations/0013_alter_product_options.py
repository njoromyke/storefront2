# Generated by Django 4.1 on 2022-08-14 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_order_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['title'], 'permissions': [('view-history', 'Can View history')]},
        ),
    ]