# Generated by Django 3.0.7 on 2020-07-02 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20200702_2153'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reply',
            old_name='comment',
            new_name='comment_on',
        ),
        migrations.AddField(
            model_name='comment',
            name='replies',
            field=models.ManyToManyField(to='core.Reply'),
        ),
    ]
