from django import template
from django.utils.html import format_html
import re

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