from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from groups.models import Group, Member, Transaction

def index(request):
    # Add an if statement to check for authentication
    t= get_template('index.html')
    html=t.render(Context({}))
    return HttpResponse(html)

