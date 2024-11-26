from django import template
from django.utils.html import format_html
from django.utils import timezone
import re
from datetime import timedelta

register = template.Library()

@register.filter(name='urlize_custom')
def urlize_custom(text):
    """Convert URLs in text into clickable links."""
    url_pattern = r'(https?://[^\s<>"]+|www\.[^\s<>"]+)'
    
    def replace_url(match):
        url = match.group(0)
        display_url = url
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        return format_html('<a href="{}" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline">{}</a>', url, display_url)
    
    return format_html(re.sub(url_pattern, replace_url, text or ''))

@register.filter(name='is_due_soon')
def is_due_soon(due_date):
    """Check if a task is due within 24 hours."""
    if not due_date:
        return False
    
    now = timezone.now()
    time_until_due = due_date - now
    return time_until_due <= timedelta(hours=24) and time_until_due > timedelta(0)