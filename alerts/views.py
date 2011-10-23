from django.views.generic.create_update import create_object
from alerts.models import Commute

def add(request):
    return create_object(request, model=Commute, login_required=True, post_save_redirect='/commutes/add')
