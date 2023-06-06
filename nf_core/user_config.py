from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from django.utils.safestring import SafeString
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .decorator import *
from .helper import *

from nf_core.models import *

"""
HELPERS
"""


def is_valid_url(to_validate: str) -> bool:
    validator = URLValidator()
    try:
        validator(to_validate)
        return True
    except ValidationError as exception:
        print(exception)
        return False


def get_BD_MNO_List() -> list:
    return [
        ("Grameenphone", "Grameenphone"),
        ("Banglalink", "Banglalink"),
        ("TeleTalk", "TeleTalk"),
        ("Robi", "Robi")
    ]


"""
AGGREGATOR - CENTRAL PLATFORM CONFIG
"""


@login_required
def setAggregatorCentralPlatformConfig(request):
    """
    SMS Configuration for AMBALAWIRELESS-INFOZILLION
    """
    operator_types = [
        "MNO",
        "IPTSP",
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
        'config_len': config_len,
        'config_list': SafeString(config_list)
    }
    return render(request, 'configuration/sms_config_aggregator_centralplatform.html', context)


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
                SmsAggregatorCentralPlatformConfig.objects.values('operator_type', 'api_key', 'send_sms_url', 'delivery_status_url', 'check_balance_url', 'check_cli_url')
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
        error = {
            'code': 500,
            'message': str(e)
        }
        return JsonResponse(error, safe=False)


"""
AGGREGATOR - OPERATOR CONFIG
"""


@login_required
def setAggregatorOperatorCredentialConfig(request):
    """
    SMS Configuration for Aggregator Operator Credentials
    """
    context = {
        'app_name': settings.APP_NAME,
        'page_title': "Aggregator Operator Credential Configuration",
        'operator_types': getOperatorTypes(),
        'all_operator_list': getOperatorList(),
        'mno_list': getOperatorList("MNO"),
        'iptsp_list': getOperatorList("IPTSP"),
    }

    return render(request, 'configuration/sms_config_aggregator_operator_credential.html', context)


def getOperatorTypes():
    return list(SmsAggregatorCentralPlatformConfig.objects.filter(operator_type="MNO").values('id', 'operator_type').order_by('-id')[:1]) \
        + list(SmsAggregatorCentralPlatformConfig.objects.filter(operator_type="IPTSP").values('id', 'operator_type').order_by('-id')[:1])


def getOperatorList(operator_type=""):
    if not operator_type:
        return list(SmsOperatorList.objects.values('operator_type', 'operator_name', 'operator_prefix'))
    else:
        return list(SmsOperatorList.objects.filter(operator_type=operator_type).values('operator_type', 'operator_name', 'operator_prefix'))


def getOperatorCredentials(operator_name=""):
    if not operator_name:
        return list(
            SmsAggregatorOperatorConfig.objects
            .values('operator_type', 'operator_name', 'operator_prefix', 'username', 'password', 'bill_msisdn', 'default_cli')
        )
    else:
        return list(
            SmsAggregatorOperatorConfig.objects.filter(operator_type=operator_name)
            .values('operator_type', 'operator_name', 'operator_prefix', 'username', 'password', 'bill_msisdn', 'default_cli')
        )


@csrf_exempt
def getAggregatorOperatorCredentialConfig(request):
    try:
        operator_name = request.POST['selected_operator_name']
        config = list(
            SmsAggregatorOperatorConfig.objects.filter(operator_name=operator_name).values('id', 'username', 'password', 'bill_msisdn', 'default_cli').order_by('-id')[:1]
        )
        return JsonResponse(config, safe=False)
    except Exception as e:
        error = {
            'code': 500,
            'message': str(e)
        }
        return JsonResponse(error, safe=False)


@login_required
@csrf_exempt
def storeAggregatorOperatorCredentialConfig(request):
    operator_type = request.POST['operator_type']
    operator_name = request.POST['operator_name']
    username = request.POST['username']
    password = request.POST['password']
    bill_msisdn = request.POST['bill_msisdn']
    default_cli = request.POST['default_cli']
    operator_prefix = request.POST['operator_prefix']
    operator_prefix_list = operator_prefix.split(",")

    try:
        for operator_prefix in operator_prefix_list:
            config_len = len(
                list(
                    SmsAggregatorOperatorConfig
                    .objects
                    .all()
                    .filter(
                        operator_type=operator_type,
                        operator_name=operator_name,
                        operator_prefix=operator_prefix,
                        username=username,
                        password=password,
                        bill_msisdn=bill_msisdn,
                        default_cli=default_cli
                    )
                )
            )

            if config_len == 0:
                config = SmsAggregatorOperatorConfig()
                config.operator_type = SmsAggregatorCentralPlatformConfig.objects.get(id=operator_type)
                config.operator_name = operator_name
                config.operator_prefix = operator_prefix
                config.username = username
                config.password = password
                config.bill_msisdn = bill_msisdn
                config.default_cli = default_cli
                config.save()

        msg = {
            'code': 200,
            'message': 'Success'
        }
        return JsonResponse(msg, safe=False)
    except Exception as e:
        error = {
            'code': 500,
            'message': str(e)
        }
        return JsonResponse(error, safe=False)


"""
USER - CLI CONFIG
"""


def getUserInfo(user_id=""):
    if not user_id:
        return list(UserInfo.objects.filter(user_group='User').values('id', 'user_id', 'company_name').order_by('id'))
    else:
        return list(UserInfo.objects.filter(id=user_id).select_related('user').values('id', 'user_id', 'company_name').order_by('-id')[:1])


def getUserCliList(user_id=""):
    if not user_id:
        return list(SmsUserCliConfig.objects.values('id', 'user_id', 'cli').order_by('id'))
    else:
        return list(SmsUserCliConfig.objects.filter(user_id=user_id).values('id', 'user_id', 'cli').order_by('-id')[:1])


@csrf_exempt
def getUserCliConfig(request):
    user_id = request.POST['user_id']
    user_cli = getUserCliList(user_id)
    return JsonResponse(user_cli, safe=False)


@login_required
def setUserCliConfig(request):
    """
    SMS Configuration for User CLI
    """
    context = {
        'app_name': settings.APP_NAME,
        'page_title': "User CLI Configuration",
        'user_info': getUserInfo(),
        'user_cli_list': getUserCliList()
    }
    return render(request, 'configuration/sms_config_user_cli.html', context)


@login_required
@csrf_exempt
def storeUserCliConfig(request):
    user_id = request.POST['user_id']
    cli = request.POST['cli']

    try:
        config_len = len(list(SmsUserCliConfig.objects.filter(user_id=user_id, cli=cli).values('user_id', 'cli')))

        if config_len == 0:
            config = SmsUserCliConfig()
            config.user_id = user_id
            config.cli = cli
            config.save()
            msg = {
                'code': 200,
                'message': 'Stored successfully'
            }
            return JsonResponse(msg, safe=False)
        else:
            msg = {
                'code': 200,
                'message': 'Already exists'
            }
            return JsonResponse(msg, safe=False)
    except Exception as e:
        error = {
            'code': 500,
            'message': str(e)
        }
        return JsonResponse(error, safe=False)


"""
USER DESTINATION OPERATOR CONFIG
"""


@login_required
def setUserOperatorConfig(request):
    """
    SMS Configuration for User Operator
    """
    context = {
        'app_name': settings.APP_NAME,
        'page_title': "User Destination Operator Configuration",
        'user_info': getUserInfo(),
        'destination_operator_list': get_BD_MNO_List(),
        'operator_list': getOperatorList()
    }
    return render(request, 'configuration/sms_config_user_operator.html', context)


@csrf_exempt
def getUserOperatorConfig(request):
    return 0


@login_required
@csrf_exempt
def storeUserOperatorConfig(request):
    return 0
