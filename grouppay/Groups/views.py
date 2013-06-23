from django.http import HttpResponse
from django.shortcuts import render

from groups.models import Member

# Index will take you to an index of your groups
def index(request):
   member = Member.objects.get(id=request.user.id)
   context = {'member' : member}
   return render(request, 'groups/index.html', context)
