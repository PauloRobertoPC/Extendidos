from django.db.models import Q
from .models import Notification
from django.contrib.auth.forms import PasswordResetForm

def context(request):
    user = request.user
    password_reset_form = PasswordResetForm()
    notification_list = {}
    if not user.is_authenticated:
        return {'notification_list': notification_list, 'password_reset_form': password_reset_form}
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
    return {'notification_list': notification_list, 'password_reset_form': password_reset_form}
