# Generated by Django 3.1.6 on 2021-06-05 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enroll', '0007_auto_20210605_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='p_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]