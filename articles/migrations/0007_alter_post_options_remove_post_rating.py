# Generated by Django 4.0 on 2021-12-20 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_alter_post_options_post_rating_alter_post_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_date']},
        ),
        migrations.RemoveField(
            model_name='post',
            name='rating',
        ),
    ]
