# Generated by Django 3.2.8 on 2021-10-06 01:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0002_auto_20210220_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='name_yer_tune',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='session.session', verbose_name='Session'),
        ),
    ]