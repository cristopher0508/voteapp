# Generated by Django 4.2 on 2023-04-25 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voteapp', '0004_voteimages_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='voteimages',
            name='vote_count_first',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='voteimages',
            name='vote_count_second',
            field=models.IntegerField(default=0),
        ),
    ]
