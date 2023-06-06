# Generated by Django 4.0.7 on 2023-06-06 04:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nf_core', '0046_smsqueuehandler_updated_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsUserCliConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cli', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'sms_config_user_cli',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='smsaggregatoroperatorconfig',
            name='default_cli',
            field=models.CharField(default='AMBALA', max_length=100),
        ),
        migrations.DeleteModel(
            name='SmsUserOperatorCredentialConfig',
        ),
        migrations.AddConstraint(
            model_name='smsusercliconfig',
            constraint=models.UniqueConstraint(fields=('user', 'cli'), name='unique_user_cli'),
        ),
    ]