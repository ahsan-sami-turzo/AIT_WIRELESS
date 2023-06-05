# Generated by Django 4.0.7 on 2023-06-04 06:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('nf_core', '0043_smsaggregatorcentralplatformconfig_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsOperatorList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operator_type', models.CharField(choices=[('MNO', 'MNO'), ('IPTSP', 'IPTSP')], default='MNO', max_length=5)),
                ('operator_name', models.CharField(max_length=50)),
                ('operator_prefix', models.CharField(max_length=4)),
            ],
            options={
                'db_table': 'sms_config_operator_list',
                'managed': True,
            },
        ),
        migrations.AddConstraint(
            model_name='smsoperatorlist',
            constraint=models.UniqueConstraint(fields=('operator_prefix',), name='unique_operator_prefix'),
        ),
    ]