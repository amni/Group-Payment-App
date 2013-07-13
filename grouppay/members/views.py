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
from transactions.models import IndividualTransaction



def friend_present(name):
    if Non_Registered_Member.objects.filter(name=name).count():
        return True
    
    return False

def index(request):
   member = Member.objects.get(user=User(id=request.user.id))
   friends= Non_Registered_Member.objects.filter(connection=member)
   friend_names= [friend.name for friend in friends]
   friends_who_owe= [friend for friend in friends if friend.amount<0]
   friends_who_lent= [friend for friend in friends if friend.amount>0]
   json_data= simplejson.dumps(friend_names, indent=4)
   print json_data
   context = {'member': member, 'friends_who_owe':friends_who_owe, 'friends_who_lent': friends_who_lent, 'friend_names':json_data}
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
   friend_name = post['borrower']
   description = post['description']
   payer = Member.objects.get(user=User.objects.get(id=request.user.id))
   amount = '%.2f' % (float(post['amount']))
   date = datetime.datetime.now()
   if not (friend_present(friend_name)):
      nonregfriend= Non_Registered_Member(name=friend_name, connection=payer, amount=0)
      nonregfriend.save()
   friend=Non_Registered_Member.objects.get(name=friend_name, connection=payer)
   if (loaning=='1'):
      friend.amount=float(friend.amount)- float(amount) 
   else: 
      friend.amount=float(friend.amount)+float(amount)  
   friend.save()
   transaction = IndividualTransaction(name= friend.name, description=description,
      amount=amount, date=date)
   transaction.save()

   return detail(request, member_id)