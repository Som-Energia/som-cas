# Generated by Django 2.2.12 on 2020-04-14 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('som_cas', '0003_auto_20200414_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='agregistration',
            name='registration_type',
            field=models.CharField(choices=[('in_person', 'In person'), ('virtual', 'Virtual')], help_text='Type of registration: if virtual or in person', max_length=15, verbose_name='Registration type'),
            preserve_default=False,
        ),
    ]
