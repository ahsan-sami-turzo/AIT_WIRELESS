import json
import os.path

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.shortcuts import render, HttpResponse
from django.utils.safestring import SafeString
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, AdminPasswordChangeForm
from rest_framework.authtoken.models import Token
from django.db.models import Sum, Count
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .decorator import *
from .forms import *
from .helper import *

from datetime import datetime, timedelta
from pprint import pprint
from operator import itemgetter
from nf_core.models import User, SmsAggregatorCentralPlatformConfig


def is_valid_url(to_validate: str) -> bool:
    validator = URLValidator()
    try:
        validator(to_validate)
        return True
    except ValidationError as exception:
        print(exception)
        return False


@login_required
def setAggregatorCentralPlatformConfig(request):
    """
    SMS Configuration for AMBALAWIRELESS-INFOZILLION
    """
    operator_types = [
        "MNO",
        "IPTSP",
    ]
    mno_list = [
        "Grameenphone",
        "Banglalink",
        "TeleTalk",
        "Robi"
    ]
    iptsp_list = [
        "Agni",
        "BanglaPhone",
        "BijoyPhone",
        "DhakaPhone",
        "NationalPhone",
        "Onetel",
        "PeoplesTel",
        "RanksTel",
        "ShebaPhone",
        "Telebarta",
    ]

    config_list = list(
        SmsAggregatorCentralPlatformConfig
        .objects
        .values('operator_type', 'api_key', 'send_sms_url', 'delivery_status_url', 'check_balance_url', 'check_cli_url')
    )
    config_len = len(config_list)

    context = {
        'app_name': settings.APP_NAME,
        'page_title': "Aggregator Central Platform Configuration",
        'operator_types': operator_types,
        'mno_list': mno_list,
        'iptsp_list': iptsp_list,
        'config_len': config_len,
        'config_list': SafeString(config_list)
    }

    return render(request, 'configuration/sms_aggregator_centralplatform_config.html', context)


@login_required
@csrf_exempt
def storeAggregatorCentralPlatformConfig(request):
    operator_type = request.POST['operator_type']
    api_key = request.POST['api_key']
    send_sms_url = request.POST['send_sms_url']
    delivery_status_url = request.POST['delivery_status_url']
    check_balance_url = request.POST['check_balance_url']
    check_cli_url = request.POST['check_cli_url']

    error = {
        'code': 500,
        'message': 'Invalid URL'
    }

    if not is_valid_url(send_sms_url):
        return JsonResponse(error, safe=False)
    if not is_valid_url(delivery_status_url):
        return JsonResponse(error, safe=False)
    if not is_valid_url(check_balance_url):
        return JsonResponse(error, safe=False)
    if operator_type == 'MNO' and not is_valid_url(check_cli_url):
        return JsonResponse(error, safe=False)

    try:
        config_list = list(
            SmsAggregatorCentralPlatformConfig
            .objects
            .all()
            .filter(
                operator_type=operator_type,
                api_key=api_key,
                send_sms_url=send_sms_url,
                delivery_status_url=delivery_status_url,
                check_balance_url=check_balance_url,
                check_cli_url=check_cli_url
            )
            .values('operator_type', 'api_key', 'send_sms_url', 'delivery_status_url', 'check_balance_url', 'check_cli_url')
        )

        config_len = len(config_list)

        if config_len == 0:
            config = SmsAggregatorCentralPlatformConfig()
            config.operator_type = operator_type
            config.api_key = api_key
            config.send_sms_url = send_sms_url
            config.delivery_status_url = delivery_status_url
            config.check_balance_url = check_balance_url
            config.check_cli_url = check_cli_url
            config.save()

            config = list(
                SmsAggregatorCentralPlatformConfig
                .objects
                .values('operator_type', 'api_key', 'send_sms_url', 'delivery_status_url', 'check_balance_url', 'check_cli_url')
            )
            msg = {
                'code': 200,
                'message': 'Stored successfully',
                'config': config
            }
            return JsonResponse(msg, safe=False)
        else:
            msg = {
                'code': 200,
                'message': 'Already exists',
                'config': config_list
            }
            return JsonResponse(msg, safe=False)
    except Exception as e:
        return JsonResponse(str(e), safe=False)


@login_required
def setUserOperatorCredentialConfig(request):
    """
    SMS Configuration for User Operator Credentials
    """
    operator_types = [
        "MNO",
        "IPTSP",
    ]
    mno_list = [
        "Grameenphone",
        "Banglalink",
        "TeleTalk",
        "Robi"
    ]
    iptsp_list = [
        "Agni",
        "BanglaPhone",
        "BijoyPhone",
        "DhakaPhone",
        "NationalPhone",
        "Onetel",
        "PeoplesTel",
        "RanksTel",
        "ShebaPhone",
        "Telebarta",
    ]
    context = {
        'app_name': settings.APP_NAME,
        'page_title': "User Operator Credential Configuration",
        'user_info': UserInfo.objects.all().order_by('id'),
        'operator_types': operator_types,
        'mno_list': mno_list,
        'iptsp_list': iptsp_list,
    }
    return render(request, 'configuration/sms_user_operator_credential_config.html', context)


@login_required
@csrf_exempt
def storeUserOperatorCredentialConfig(request):
    return JsonResponse(str('aaa'), safe=False)
