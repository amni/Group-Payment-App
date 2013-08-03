from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404

import datetime

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import pdb
from groups.models import Group
from members.models import Member
from transactions.model import Transaction

import pdb

def addLoan(request, group_id):
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
   transaction = Transaction(name= nonregfriend.name, description=description, group=group,
      payer=payer,amount=amount, date=date)
   transaction.save()

   return detail(request, group_id)

def addDebt(request, group_id):
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
   nonregfriend.amount=float(nonregfriend.amount)+ float(amount)   
   transaction = Transaction(name= nonregfriend.name, description=description, group=group,
      payer=payer,amount=amount, date=date)
   transaction.save()

   return detail(request, group_id)