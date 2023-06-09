# Generated by Django 2.2.12 on 2023-05-18 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0013_auto_20230518_1007'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='inst',
            new_name='institution',
        ),
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='donor.Status', to_field='code'),
        ),
    ]
