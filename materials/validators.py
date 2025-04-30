import re

from rest_framework.serializers import ValidationError


class LinkValidator:
    """
    Adding validator to check url link for lesson to lead for youtube.com
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        link = value.get("url_link")
        if link:
            if "://youtube.com" not in value.get("url_link"):
                raise ValidationError(
                    "The only possible links is possibly for youtube.com"
                )
