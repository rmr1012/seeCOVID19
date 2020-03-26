# Generated by Django 2.0.3 on 2020-03-26 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='locationData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('count', models.IntegerField()),
                ('type', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='logFitCache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('countryCode', models.CharField(max_length=5)),
                ('province', models.CharField(max_length=20, null=True)),
                ('city', models.CharField(max_length=25, null=True)),
                ('addedTimestamp', models.DateTimeField(auto_now_add=True)),
                ('email', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='mapData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=40)),
                ('province', models.CharField(max_length=40, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='subscriberList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('countryCode', models.CharField(max_length=5)),
                ('province', models.CharField(max_length=20, null=True)),
                ('city', models.CharField(max_length=25, null=True)),
                ('addedTimestamp', models.DateTimeField(auto_now_add=True)),
                ('email', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='mapdata',
            unique_together={('country', 'province')},
        ),
        migrations.AddField(
            model_name='locationdata',
            name='locationID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seeCOVID19.mapData'),
        ),
        migrations.AlterUniqueTogether(
            name='locationdata',
            unique_together={('locationID', 'date', 'type')},
        ),
    ]
