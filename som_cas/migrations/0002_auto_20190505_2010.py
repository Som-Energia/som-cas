# Generated by Django 2.2 on 2019-05-05 20:10

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('som_cas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_file', models.FileField(help_text='File in json format with all register members for the virtual assambley', upload_to=settings.UPLOAD_DIR, verbose_name='Registration file')),
            ],
        ),
        migrations.AlterField(
            model_name='somuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]
