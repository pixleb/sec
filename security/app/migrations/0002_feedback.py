# Generated by Django 4.1.4 on 2023-07-13 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imageSource', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=64)),
                ('feedSource', models.CharField(max_length=256)),
            ],
        ),
    ]
