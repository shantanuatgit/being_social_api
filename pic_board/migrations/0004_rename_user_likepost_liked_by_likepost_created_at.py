# Generated by Django 4.2.2 on 2023-10-03 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pic_board', '0003_likepost'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likepost',
            old_name='user',
            new_name='liked_by',
        ),
        migrations.AddField(
            model_name='likepost',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
    ]
