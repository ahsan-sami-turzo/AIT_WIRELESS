import uuid

from django.contrib.auth.models import User
from django.db import models
from psqlextra.types import PostgresPartitioningMethod
from psqlextra.models import PostgresPartitionedModel


def generate_filename(instance, filename):
    """
    Generate random file name
    """
    extension = filename.split('.')[-1]
    new_filename = "nf_%s.%s" % (uuid.uuid4(), extension)
    return new_filename


class UserInfo(models.Model):
    """
    Extended table to handle the user info
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_info')
    mobile = models.CharField(max_length=11)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    config_status = models.BooleanField(default=False, null=True, blank=True)
    credit = models.FloatField(default=0, null=True, blank=True)
    expiry_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_image = models.ImageField(default='defaults/user.png', upload_to=generate_filename, null=True, blank=True)
    user_group = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = 'User Info'
        verbose_name_plural = 'User Info'
        indexes = [models.Index(fields=['user', 'mobile'])]


class SenderID(models.Model):
    """
    List of Sender IDs
    """
    sender_id = models.CharField(max_length=13, unique=True)
    default = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender_id

    class Meta:
        verbose_name = 'Sender ID'
        verbose_name_plural = 'Sender ID'
        indexes = [models.Index(fields=['sender_id'])]


class DefaultSMSRate(models.Model):
    """
    Default SMS Rate
    """
    operator_name = models.CharField(max_length=200)
    operator_prefix = models.CharField(max_length=200)
    masking_sms_rate = models.FloatField(default=0)
    non_masking_sms_rate = models.FloatField(default=0)

    def __str__(self):
        return "Default SMS Rate"

    class Meta:
        verbose_name = 'Default SMS Rate'
        verbose_name_plural = 'Default SMS Rate'
        indexes = [models.Index(fields=['operator_name', 'operator_prefix'])]


class SMSQueue(models.Model):
    """
    SMS Queue Management
    """
    name = models.CharField(max_length=200)
    queue = models.CharField(max_length=200, unique=True)
    usage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'SMS Route'
        verbose_name_plural = 'SMS Route'


class UserSMSRate(models.Model):
    """
    SMS rate for user (Many to Many)
    """
    operator = models.CharField(max_length=200)
    prefix = models.CharField(max_length=5)
    masking_rate = models.FloatField()
    non_masking_rate = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class UserConfig(models.Model):
    """
    User configuration for sending SMS
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_config')
    queue = models.ForeignKey(SMSQueue, on_delete=models.PROTECT, related_name='user_queue', null=True, blank=True)
    sender_id = models.ManyToManyField(SenderID, blank=True)
    sms_rate = models.ManyToManyField(UserSMSRate, blank=True)
    priority = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Configuration'
        verbose_name_plural = 'User Configuration'


class ContactGroup(models.Model):
    """
    Group for Contacts
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_contact_group')
    group_name = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Contact Group'
        verbose_name_plural = 'Contact Group'


class Contacts(models.Model):
    """
    Contact Management
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_contacts')
    group = models.ForeignKey(ContactGroup, on_delete=models.CASCADE, related_name='group_contact')
    name = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=14)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Contacts'
        verbose_name_plural = 'Contacts'
        indexes = [models.Index(fields=['user', 'name', 'mobile'])]


class SMSHistory(PostgresPartitionedModel):
    """
    SMS History of a user

    Default "Pending"
    On submit "Submitted"
    On processing "Processing"
    On delivery complete "Delivered"
    On failure "Failed"
    On Scheduled "Scheduled"

    sms_category = masking/non-masking
    sms_type = text/unicode
    """
    uid = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_sms_history')
    sms_queue = models.CharField(max_length=200, null=True, blank=True)
    shoot_id = models.CharField(max_length=200, null=True, blank=True)
    receiver = models.CharField(max_length=200)
    sender_id = models.CharField(max_length=200, null=True, blank=True)
    operator_name = models.CharField(max_length=200, null=True, blank=True)
    sms_category = models.CharField(max_length=200, null=True)
    sms_type = models.CharField(max_length=200)
    sms_length = models.IntegerField()
    sms_count = models.IntegerField()
    sms_body = models.TextField()
    sms_body_encoded = models.TextField()
    sms_rate = models.FloatField(default=0)
    sms_cost = models.FloatField()
    status = models.CharField(max_length=200, default='Pending')
    failure_reason = models.TextField(null=True, blank=True)
    scheduled = models.BooleanField(default=False)
    scheduled_time = models.DateTimeField(null=True, blank=True)
    scheduled_params = models.TextField(null=True, blank=True)
    api_response = models.JSONField(default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['user', 'receiver', 'sender_id', 'status', 'scheduled']),
                   models.Index(fields=['created_at'])]

    class PartitioningMeta:
        method = PostgresPartitioningMethod.RANGE
        key = ["created_at"]


class SMSSchedule(models.Model):
    """
    SMS Schedule Handler
    """
    sms_id = models.IntegerField()
    sms_queue = models.CharField(max_length=200)
    params = models.TextField(null=True, blank=True)
    scheduled_time = models.DateTimeField(null=True, blank=True)
    executed = models.BooleanField(default=False)


class BlockKeyword(models.Model):
    """
    Block keyword from SMS Content
    """
    keywords = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


class SMSTemplate(models.Model):
    """
    Predefined SMS Template
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sms_template')
    template_name = models.CharField(max_length=200)
    sms_body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserRechargeHistory(PostgresPartitionedModel):
    """
    All recharge history of users
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_recharge_history')
    payment_method = models.CharField(max_length=200, null=True, blank=True)
    trx_id = models.CharField(max_length=200, null=True, blank=True)
    trx_type = models.CharField(max_length=200, null=True, blank=True)
    recharge_amount = models.FloatField()
    previous_balance = models.FloatField(default=0, null=True, blank=True)
    new_balance = models.FloatField(default=0, null=True, blank=True)
    balance_expiry_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['user', 'trx_id']), models.Index(fields=['created_at'])]

    class PartitioningMeta:
        method = PostgresPartitioningMethod.RANGE
        key = ["created_at"]


class UserLoginSession(models.Model):
    """
    User login session handler
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_session')
    key = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class SMSQueueHandler(models.Model):
    """
    SMS Queue handler for preview
    """
    sms_id = models.IntegerField()
    user_id = models.IntegerField(default=0)
    username = models.CharField(max_length=200)
    sms_count = models.IntegerField(default=1)
    queue = models.CharField(max_length=200)
    operator_logo = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# SMS CONFIG START
# Date: 24-05-2023 - 06-06-2023

class SmsAggregatorCentralPlatformConfig(models.Model):
    """
    SMS Configuration for AMBALAWIRELESS-INFOZILLION
    """
    api_key = models.CharField(max_length=200)
    operator_type = models.CharField(default="MNO", max_length=5)
    default_bill_msisdn = models.CharField(blank=False, null=False, max_length=100)
    send_sms_url = models.URLField(blank=False, null=False, default="https://api.mnpspbd.com/a2p-sms/api/v1/send-sms")
    delivery_status_url = models.URLField(default="https://api.mnpspbd.com/a2p-proxy-api/api/v1/check-delivery-report")
    check_balance_url = models.URLField(default="https://api.mnpspbd.com/a2p-proxy-api/api/v1/check-credit-balance")
    check_cli_url = models.URLField(default="https://api.mnpspbd.com/a2p-proxy-api/api/v1/check-cli")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "sms_config_aggregator_centralplatform"
        indexes = [models.Index(fields=['operator_type'])]


class SmsAggregatorOperatorConfig(models.Model):
    """
    SMS Configuration for AMBALAWIRELESS-MNO/IPTSP
    """
    operator_type = models.ForeignKey(SmsAggregatorCentralPlatformConfig, on_delete=models.CASCADE)
    operator_name = models.CharField(blank=False, null=False, max_length=100)
    operator_prefix = models.CharField(blank=False, null=False, max_length=10)
    username = models.CharField(blank=False, null=False, max_length=100)
    password = models.CharField(blank=False, null=False, max_length=100)
    bill_msisdn = models.CharField(blank=False, null=False, max_length=100)
    default_cli = models.CharField(blank=False, null=False, max_length=100, default="AMBALA")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "sms_config_aggregator_operator"
        indexes = [models.Index(fields=['operator_prefix'])]


class SmsUserCliConfig(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cli = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "sms_config_user_cli"
        constraints = [
            models.UniqueConstraint(fields=['user', 'cli'], name='unique_user_cli')
        ]


class SmsUserDestinationOperatorConfig(models.Model):
    """
    SMS Configuration for Destination
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    destination_operator_name = models.CharField(blank=False, null=False, max_length=100)
    destination_operator_prefix = models.CharField(max_length=10)
    aggregator_operator = models.ForeignKey(SmsAggregatorOperatorConfig, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "sms_config_user_destination_operator"
        indexes = [models.Index(fields=['user', 'destination_operator_prefix'])]
        constraints = [
            models.UniqueConstraint(fields=['user', 'destination_operator_prefix'], name='unique_user_destinationoperator')
        ]


class SmsOperatorList(models.Model):
    """
    MNO/IPTSP LIST
    """
    operator_type = models.CharField(default="MNO", max_length=5)
    operator_name = models.CharField(blank=False, null=False, max_length=100)
    operator_prefix = models.CharField(max_length=10)

    class Meta:
        managed = True
        db_table = "sms_config_operator_list"
        constraints = [
            models.UniqueConstraint(fields=['operator_prefix'], name='unique_operator_prefix')
        ]
