# Generated by Django 4.0.7 on 2023-05-28 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nf_core', '0042_smsschedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsAggregatorCentralPlatformConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(max_length=50)),
                ('operator_type', models.CharField(choices=[('MNO', 'MNO'), ('IPTSP', 'IPTSP')], default='MNO', max_length=5)),
                ('send_sms_url', models.URLField(default='https://api.mnpspbd.com/a2p-sms/api/v1/send-sms')),
                ('delivery_status_url', models.URLField(default='https://api.mnpspbd.com/a2p-proxy-api/api/v1/check-delivery-report')),
                ('check_balance_url', models.URLField(default='https://api.mnpspbd.com/a2p-proxy-api/api/v1/check-credit-balance')),
                ('check_cli_url', models.URLField(default='https://api.mnpspbd.com/a2p-proxy-api/api/v1/check-cli')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'SMS Aggregator Central Platform Config',
                'db_table': 'sms_aggregator_centralplatform_config',
                'get_latest_by': ['id'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SmsAggregatorOperatorConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operator_name', models.CharField(max_length=20)),
                ('operator_prefix', models.CharField(max_length=4, unique=True)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('bill_msisdn', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('operator_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nf_core.smsaggregatorcentralplatformconfig')),
            ],
            options={
                'verbose_name': 'SMS Aggregator MNO/IPTSP Config',
                'db_table': 'sms_aggregator_operator_config',
                'get_latest_by': ['id'],
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='smsqueuehandler',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='SmsUserOperatorCredentialConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_masking_enabled', models.BooleanField(default=False)),
                ('cli', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('operator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nf_core.smsaggregatoroperatorconfig')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'SMS User Operator Credential Config',
                'db_table': 'sms_user_operator_credential_config',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SmsUserDestinationConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination_operator_name', models.CharField(choices=[('Grameenphone', 'Grameenphone'), ('Banglalink', 'Banglalink'), ('TeleTalk', 'TeleTalk'), ('Robi', 'Robi')], max_length=20)),
                ('destination_operator_prefix', models.CharField(max_length=3)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('aggregator_operator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nf_core.smsaggregatoroperatorconfig')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'SMS User Destination Config',
                'db_table': 'sms_user_destination_config',
                'managed': True,
            },
        ),
        migrations.AddIndex(
            model_name='smsaggregatorcentralplatformconfig',
            index=models.Index(fields=['operator_type'], name='sms_aggrega_operato_eddaef_idx'),
        ),
        migrations.AddIndex(
            model_name='smsuseroperatorcredentialconfig',
            index=models.Index(fields=['user', 'operator'], name='sms_user_op_user_id_126481_idx'),
        ),
        migrations.AddIndex(
            model_name='smsuserdestinationconfig',
            index=models.Index(fields=['user', 'destination_operator_prefix'], name='sms_user_de_user_id_1f8e1b_idx'),
        ),
        migrations.AddIndex(
            model_name='smsaggregatoroperatorconfig',
            index=models.Index(fields=['operator_prefix'], name='sms_aggrega_operato_23916a_idx'),
        ),
    ]
