# Generated by Django 3.1.6 on 2023-06-08 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0010_auto_20230530_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='reset_password_token',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='advertises',
            name='description',
            field=models.CharField(max_length=4000),
        ),
        migrations.AlterField(
            model_name='contact',
            name='message',
            field=models.CharField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='crackgame',
            name='description',
            field=models.CharField(max_length=4000),
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='game',
            name='description',
            field=models.CharField(max_length=4000),
        ),
        migrations.AlterField(
            model_name='news',
            name='description',
            field=models.CharField(max_length=4000),
        ),
        migrations.AlterField(
            model_name='orders',
            name='mobile',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='useradvertises',
            name='description',
            field=models.CharField(max_length=4000),
        ),
    ]