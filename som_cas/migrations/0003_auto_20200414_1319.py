# Generated by Django 2.2.12 on 2020-04-14 13:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('som_cas', '0002_auto_20190505_2010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agregistration',
            name='registration_file',
        ),
        migrations.AddField(
            model_name='agregistration',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, help_text='Member registration date', verbose_name='Registration date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agregistration',
            name='member',
            field=models.ForeignKey(help_text='Member for this registration', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Member'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Assambley',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the assambley, eg: Asamblea 2020', max_length=150, unique_for_year='date', verbose_name='Assambley name')),
                ('date', models.DateField(help_text='Date when this occurrence end', verbose_name='Start time')),
                ('active', models.BooleanField(help_text='Assembley state', verbose_name='Active')),
                ('registered', models.ManyToManyField(through='som_cas.AgRegistration', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='agregistration',
            name='assambley',
            field=models.ForeignKey(help_text='Assambley for this registration', on_delete=django.db.models.deletion.CASCADE, to='som_cas.Assambley', verbose_name='Assambley'),
            preserve_default=False,
        ),
    ]
