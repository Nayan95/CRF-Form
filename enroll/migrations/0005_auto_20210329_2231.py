# Generated by Django 3.1.7 on 2021-03-29 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enroll', '0004_auto_20210327_0758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='ans_text',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
