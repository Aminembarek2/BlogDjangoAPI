# Generated by Django 4.0 on 2021-12-20 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_user_groups_user_is_superuser_user_user_permissions'),
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.user'),
        ),
    ]
