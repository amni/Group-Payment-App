from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404

from django.core.urlresolvers import reverse

from groups.models import Member, Group, Transaction

import pdb;
def index(request):
   try:
      member = Member.objects.get(id=request.user.id)
      groups = member.groups.all()
      context = {'member' : member, 'groups': groups}
   except Member.DoesNotExist:
      context = {}
   return render(request, 'groups/index.html', context)

def detail(request, group_id):
   try:
      group = Group.objects.get(id=group_id)
      member = Member.objects.get(id=request.user.id)
      context = {'member': member, 'group': group}
   except Group.DoesNotExist:
      raise Http404
   return render(request, 'groups/detail.html', context)

def addgroup(request):
   if 'groupname' in request.POST:
      groupname = request.POST['groupname']

      # Create the new group
      group = Group(name=groupname)
      group.save()

      # Add the current user to the group
      member = Member.objects.get(id=request.user.id)
      member.groups.add(group)

      return detail(request, group.id)
   else:
      # TODO: Add some sort of error here. Group name is empty.
      return index(request)
