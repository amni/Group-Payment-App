from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404

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
      transaction= Transaction.objects.get(id=request.user.id)
      context = {'member': member, 'group': group, 'transactions': transactions(transaction)}
   except Group.DoesNotExist:
      raise Http404
   return render(request, 'groups/detail.html', context)


def sumTransactions(transactions):
   integerList= [int (transaction) for transaction in transactions]
   return integerList


