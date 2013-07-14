from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404

import datetime

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from groups.models import Group
from members.models import Member, Non_Registered_Member
from transactions.models import Transaction
import pdb

def friend_present(name):
    friend=Non_Registered_Member.objects.filter(name=name)
    if friend.count():
         return True
    
    return False

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
      friends= Non_Registered_Member.objects.filter(connection=member)
      member_balances={}
      transaction_total= calculateTransactions(transactions, group_members, member_balances)
      print (transaction_total)
      print (member_balances)
      context = {'member': member, 'group': group,
      'group_members': group_members, 'transactions': transactions,
      'transactions_count': len(transactions), 'member_balances':member_balances, 'friends':friends}
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
   friend_name = post['borrower']
   description = post['description']
   group = Group.objects.get(id=group_id)
   payer = Member.objects.get(user=User.objects.get(id=request.user.id))
   amount = '%.2f' % (float(post['amount']))
   date = datetime.datetime.now()
   if not (friend_present(friend_name)):
      nonregfriend= Non_Registered_Member(name=friend_name, connection=payer, amount=0)
      nonregfriend.save()
   nonregfriend=Non_Registered_Member.objects.get(name=friend_name, connection=payer)
   nonregfriend.amount=float(nonregfriend.amount)- float(amount)   
   nonregfriend.save()
   transaction = Transaction(name= nonregfriend.name, description=description, group=group,
      payer=payer,amount=amount, date=date)
   transaction.save()

   return detail(request, group_id)

def addMember(request, group_id):
   #Adds user if email corresponds to a user in the database
   post = request.POST
   user= Member.objects.get(user=User.objects.get(id=request.user.id))
   friend_name= post['friend']
   group = Group.objects.get(id=group_id)
   if not (friend_present(friend_name)):
      nonregfriend= Non_Registered_Member(name=friend_name, connection=user, amount=0)
      nonregfriend.save()
   friend=  Non_Registered_Member.objects.get(name=friend_name, connection=user)
   friend.groups.add(group)
   friend.save()
   return detail(request, group_id)


def calculateTransactions(transactions, group_members, member_balances):
   #TODO: Rewrite this so that it only iterates through transaction once, instead of once for every member
   total_transactions= sum([transaction.amount for transaction in transactions])
   for member in group_members:
      member_balances[member]= total_transactions/len(group_members)-sum([transaction.amount for transaction in transactions if transaction.payer==member])
   return total_transactions

