# Generated by Django 5.0.1 on 2024-03-08 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpost',
            old_name='head0',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='blogpost',
            old_name='head1',
            new_name='heading',
        ),
        migrations.RenameField(
            model_name='blogpost',
            old_name='head2',
            new_name='subheading',
        ),
    ]
