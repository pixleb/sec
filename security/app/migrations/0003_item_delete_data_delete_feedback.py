# Generated by Django 4.1.4 on 2023-07-19 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('material', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=124)),
                ('src', models.CharField(max_length=64)),
            ],
        ),
        migrations.DeleteModel(
            name='Data',
        ),
        migrations.DeleteModel(
            name='FeedBack',
        ),
    ]
