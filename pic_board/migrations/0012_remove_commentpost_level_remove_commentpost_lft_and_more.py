# Generated by Django 4.2.2 on 2023-10-08 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pic_board', '0011_rename_reply_to_comment_commentpost_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentpost',
            name='level',
        ),
        migrations.RemoveField(
            model_name='commentpost',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='commentpost',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='commentpost',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='commentpost',
            name='tree_id',
        ),
        migrations.AddField(
            model_name='commentpost',
            name='reply_to_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='pic_board.commentpost'),
        ),
    ]
