# Generated by Django 3.1.6 on 2023-05-31 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0007_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAdvertises',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customerId', models.PositiveIntegerField(null=True)),
                ('title', models.CharField(max_length=40)),
                ('adv_image', models.ImageField(blank=True, null=True, upload_to='adv_image/')),
                ('posted_date', models.DateField(auto_now_add=True, null=True)),
                ('description', models.CharField(max_length=40)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
    ]