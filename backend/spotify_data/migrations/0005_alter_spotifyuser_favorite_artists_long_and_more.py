# Generated by Django 4.1 on 2024-11-05 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify_data', '0004_spotifyuser_favorite_genres_long_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spotifyuser',
            name='favorite_artists_long',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='spotifyuser',
            name='favorite_artists_medium',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='spotifyuser',
            name='favorite_artists_short',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='spotifyuser',
            name='favorite_genres_long',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='spotifyuser',
            name='favorite_genres_medium',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='spotifyuser',
            name='favorite_genres_short',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='spotifyuser',
            name='favorite_tracks_long',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='spotifyuser',
            name='favorite_tracks_medium',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='spotifyuser',
            name='favorite_tracks_short',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='spotifyuser',
            name='quirkiest_artists_long',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='spotifyuser',
            name='quirkiest_artists_medium',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='spotifyuser',
            name='quirkiest_artists_short',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]