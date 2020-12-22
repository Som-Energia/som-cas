# Generated by Django 2.2.17 on 2020-12-22 12:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('som_cas', '0007_auto_20201204_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='assembly',
            name='end_votation_date',
            field=models.DateTimeField(blank=True, help_text='Date and hour when the votation of this assembly ends', null=True, verbose_name='Votation end date'),
        ),
        migrations.AddField(
            model_name='assembly',
            name='start_votation_date',
            field=models.DateTimeField(blank=True, help_text='Date and hour when the votation of this assembly starts', null=True, verbose_name='Votation start date'),
        ),
        migrations.AlterField(
            model_name='agregistration',
            name='assembly',
            field=models.ForeignKey(help_text='Assembly for this registration', on_delete=django.db.models.deletion.CASCADE, to='som_cas.Assembly', verbose_name='Assembly'),
        ),
        migrations.AlterField(
            model_name='agregistration',
            name='date',
            field=models.DateField(auto_now_add=True, help_text='Member registration date', verbose_name='Registration date'),
        ),
        migrations.AlterField(
            model_name='agregistration',
            name='member',
            field=models.ForeignKey(help_text='Member for this registration', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Member'),
        ),
        migrations.AlterField(
            model_name='agregistration',
            name='registration_email_sent',
            field=models.BooleanField(default=False, help_text='Check if registration email was sent to the member', verbose_name='Sent registration email'),
        ),
        migrations.AlterField(
            model_name='agregistration',
            name='registration_type',
            field=models.CharField(choices=[('in_person', 'In person'), ('virtual', 'Virtual')], help_text='Type of registration: if virtual or in person', max_length=15, verbose_name='Registration type'),
        ),
        migrations.AlterField(
            model_name='assembly',
            name='date',
            field=models.DateField(help_text='Date and hour of this assembly', verbose_name='Assembly date'),
        ),
    ]
