# Generated by Django 4.0.1 on 2022-01-14 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tweetApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tweetApp.tweet'),
        ),
    ]
