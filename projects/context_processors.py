from django.db.models import Q
from .models import Notification

def notification_list(request):
    user = request.user
    notification_list = {}
    if not user.is_authenticated:
        return {'notification_list': notification_list}
    if(user.is_ong):
        notification_list = Notification.objects.filter(
            Q(state='UNREAD'),
            Q(job__project__ong=request.user.ong),
            Q(directed_to_student=False)
        )
    else:
        notification_list =  Notification.objects.filter(
            Q(state='UNREAD'),
            Q(student__user=user),
            Q(directed_to_student=True)
        )
    return {'notification_list': notification_list}
