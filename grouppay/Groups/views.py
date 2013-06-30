from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404

import datetime

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import pdb
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
      member_balances={}
      transaction_total= calculateTransactions(transactions, group_members, member_balances)
      print (transaction_total)
      print (member_balances)
      context = {'member': member, 'group': group,
      'group_members': group_members, 'transactions': transactions,
      'transactions_count': len(transactions), 'member_balances':member_balances}
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
   amount = '%.2f' % (float(post['amount']))
   print amount 
   date = datetime.datetime.now()

   transaction = Transaction(name=name, description=description, group=group,
      payer=payer, amount=amount, date=date)
   transaction.save()

   return detail(request, group_id)

def addMember_email(request, group_id):
   #Adds user if email corresponds to a user in the database
   if (User.objects.get(email=request.user.email)):
      post = request.POST 
      email = post ['email']
      group = Group.objects.get(id=group_id)
      member= Member.objects.get(user=User.objects.get(email=email))
      member.groups.add(group)
   #TODO: add error message
   else:
      pass
   return detail(request, group_id)

def addMember_username(request, group_id):
   #Adds user if username corresponds to a user in the database
   if (User.objects.get(username=request.user.username)):
      post = request.POST 
      username = post ['username']
      group = Group.objects.get(id=group_id)
      member= Member.objects.get(user=User.objects.get(username=username))
      member.groups.add(group)
   #TODO: add error message
   else:
      pass
   return detail(request, group_id)

def calculateTransactions(transactions, group_members, member_balances):
   #TODO: Rewrite this so that it only iterates through transaction once, instead of once for every member 
   total_transactions= sum([transaction.amount for transaction in transactions])
   for member in group_members:
      member_balances[member]= total_transactions/len(group_members)-sum([transaction.amount for transaction in transactions if transaction.payer==member])
   return total_transactions
