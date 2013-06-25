from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404

import datetime

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

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
      group_members = Member.objects.filter(groups=Group.objects.get(id=group_id))
      transactions = Transaction.objects.filter(group=Group.objects.get(id=group_id))
      context = {'member': member, 'group': group,
      'group_members': group_members, 'transactions': transactions,
      'transactions_count': len(transactions)}
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
      # Make sure to use user instead of id b/c not equal
      member = Member.objects.get(user=User.objects.get(id=request.user.id))
      member.groups.add(group)

      return detail(request, group.id)
   else:
      # TODO: Add some sort of error here. Group name is empty.
      return index(request)

# TODO: Add checks on the incoming values.
# TODO: Try/Catch block?
def addTransaction(request, group_id):
   post = request.POST
   name = post['name']
   description = post['description']
   group = Group.objects.get(id=group_id)
   payer = Member.objects.get(user=User.objects.get(id=request.user.id))
   amount = post['amount']
   date = datetime.datetime.now()

   transaction = Transaction(name=name, description=description, group=group,
      payer=payer, amount=amount, date=date)
   transaction.save()

   return detail(request, group_id)

def addMember_email(request, group_id):
   # TODO: FILL THIS IN
   return detail(request, group_id)

def addMember_username(request, group_id):
   # TODO: FILL THIS IN
   return detail(request, group_id)

def sumTransactions(transactions):
   integerList= [int (transaction) for transaction in transactions]
   return integerList
