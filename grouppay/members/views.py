from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.http import Http404
from django.template import Context

from django.utils import simplejson 


import datetime

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from groups.models import Group
from members.models import Member, Non_Registered_Member
from transactions.models import Transaction



def friend_present(name):
   if Non_Registered_Member.objects.filter(name=name).count():
      return True
    
   return False

def group_present(name):
    if Group.objects.filter(name=name).count():
        return True
    
    return False

def index(request):
   member = Member.objects.get(user=User(id=request.user.id))
   friends= Non_Registered_Member.objects.filter(connection=member)
   friend_names= [friend.name for friend in friends]
   friends_who_owe= [friend for friend in friends if friend.amount < 0]
   friends_who_lent= [friend for friend in friends if friend.amount > 0]
   for group in Group.objects.all():
      friend_names.append(group.name)
   json_data= simplejson.dumps(friend_names, indent=4)

   balance = 0
   owe = 0
   owe_count = 0
   lent = 0
   lent_count = 0

   for friend in friends:
      balance += friend.amount
      if friend.amount > 0:
         lent_count = lent_count + 1
         lent += friend.amount
      else:
         owe_count = owe_count + 1
         owe -= friend.amount

   print balance
   context = {'member': member, 'friends_who_owe':friends_who_owe,
    'friends_who_lent': friends_who_lent, 'friend_names':json_data, 'balance': balance,
    'lent': lent, 'owe': owe, 'lent_count': lent_count, 'owe_count': owe_count}
   return render(request, 'members/index.html', context)


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
def addTransaction(request, member_id, loaning):
   post = request.POST
   name = post['borrower']
   description = post['description']
   payer = Member.objects.get(user=User.objects.get(id=request.user.id))
   amount = '%.2f' % (float(post['amount']))
   date = datetime.datetime.now()
   if (group_present(name)):
      group=Group.objects.filter(name=name)[0]
      addGroupTransaction(group, loaning, amount)
      transaction = Transaction(description=description, amount=amount, group=group, date=date)
      transaction.save()
      return index(request)
   if not (friend_present(name)):
      nonregfriend= Non_Registered_Member(name=name, connection=payer, amount=0)
      nonregfriend.save()
   friend=Non_Registered_Member.objects.get(name=name, connection=payer)
   calculateFriendBalance(friend, loaning, amount)
   transaction = Transaction(description=description,
      amount=amount, friend=friend, date=date)
   transaction.save()

   return index(request)

def addGroupTransaction(group, loaning, amount):
   for friend in Non_Registered_Member.objects.filter(groups=group):
      calculateFriendBalance(friend, loaning, float(amount)/Non_Registered_Member.objects.count())
   
def calculateFriendBalance(friend, loaning, amount):
   if (loaning=='1'):
      friend.amount=float(friend.amount)- float(amount) 
   else: 
      friend.amount=float(friend.amount)+float(amount)
   friend.save()