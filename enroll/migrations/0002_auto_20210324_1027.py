# Generated by Django 3.1.7 on 2021-03-24 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enroll', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='p_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='enroll.patient'),
        ),
    ]
