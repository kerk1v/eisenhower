from django import template
from django.utils.html import format_html, mark_safe
from django.utils import timezone
import re
from datetime import timedelta
import markdown
from django.utils.safestring import mark_safe

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

@register.filter(name='markdown_safe')
def markdown_safe(text):
    """Convert markdown text to safe HTML with target="_blank" links."""
    if not text:
        return ''

    # Convert markdown to HTML
    md = markdown.Markdown(
        extensions=['fenced_code', 'tables', 'nl2br'],
        output_format='html5'
    )
    html = md.convert(text)

    # Add target="_blank" and styling to links
    html = re.sub(
        r'<a([^>]+)>',
        r'<a\1 target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline">',
        html
    )

    return mark_safe(html)

@register.filter(name='is_due_soon')
def is_due_soon(due_date):
    """Check if a task is due within 24 hours."""
    if not due_date:
        return False
    
    now = timezone.now()
    time_until_due = due_date - now
    return time_until_due <= timedelta(hours=24) and time_until_due > timedelta(0)