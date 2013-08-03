from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from members import views as member_view

def index(request):
    # Check to see if they are logged in
	if (request.user.id):
		return member_view.index(request)
	else:
		t= get_template('index.html')
		html=t.render(Context({}))
		return HttpResponse(html)

