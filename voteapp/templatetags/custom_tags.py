from django import template
from ..models import Notification

register = template.Library()

@register.inclusion_tag('show_notifications.html', takes_context=True)
def show_notifications(context):
    request_user = context['request'].user.profile.user_id
    notifications = Notification.objects.filter(to_user_id=request_user).exclude(user_has_seen=True).order_by('-created')
    return {'notifications': notifications}
