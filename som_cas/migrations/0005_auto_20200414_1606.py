# Generated by Django 2.2.12 on 2020-04-14 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('som_cas', '0004_agregistration_registration_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assembly',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the assembly, eg: Asamblea 2020', max_length=150, unique_for_year='date', verbose_name='Assembly name')),
                ('date', models.DateField(help_text='Date when this occurrence end', verbose_name='Start time')),
                ('active', models.BooleanField(help_text='Assembley state', verbose_name='Active')),
            ],
        ),
        migrations.RemoveField(
            model_name='agregistration',
            name='assambley',
        ),
        migrations.DeleteModel(
            name='Assambley',
        ),
        migrations.AddField(
            model_name='assembly',
            name='registered',
            field=models.ManyToManyField(through='som_cas.AgRegistration', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='agregistration',
            name='assembly',
            field=models.ForeignKey(help_text='Assembly for this registration', on_delete=django.db.models.deletion.CASCADE, to='som_cas.Assembly', verbose_name='Assembly'),
            preserve_default=False,
        ),
    ]
