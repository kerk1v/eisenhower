from django import template
from datetime import datetime, timedelta
from django.utils import timezone

register = template.Library()

@register.filter
def is_due_soon(value):
    if not value:
        return False
    now = timezone.now()
    two_days_from_now = now + timedelta(days=2)
    return value <= two_days_from_now