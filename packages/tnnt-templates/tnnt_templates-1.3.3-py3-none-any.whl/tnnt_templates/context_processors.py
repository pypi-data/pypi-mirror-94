"""
tnnt template settings
"""

from django.conf import settings


def tnnt_settings(request):
    return_value = dict()

    try:
        return_value["TNNT_TEMPLATE_ENTITY_LOGO"] = settings.TNNT_TEMPLATE_ENTITY_LOGO
    except AttributeError:
        return_value[
            "TNNT_TEMPLATE_ENTITY_LOGO"
        ] = "https://images.evetech.net/corporations/98000030/logo"

    try:
        return_value[
            "TNNT_TEMPLATE_URLS_TNNT_WEBSITES"
        ] = settings.TNNT_TEMPLATE_URLS_TNNT_WEBSITES
    except AttributeError:
        pass

    try:
        return_value[
            "TNNT_TEMPLATE_URLS_OTHER_WEBSITES"
        ] = settings.TNNT_TEMPLATE_URLS_OTHER_WEBSITES
    except AttributeError:
        pass

    return return_value
