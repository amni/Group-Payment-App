from django.db import models
from registration.signals import user_registered
from django.contrib.auth.models import User
from django.dispatch import receiver



# Create your models here.
class Group(models.Model):
   name = models.CharField(max_length=100)

   def __unicode__(self):
      return self.name

class Member(models.Model):
   # Connect the member model to the user profile
   user = models.OneToOneField('auth.User')

   # Additional member attributes
   groups = models.ManyToManyField(Group)

   def __unicode__(self):
      return self.user.get_full_name()


@receiver(user_registered)
def createMember(sender, user, request, **kwargs):
   print user
   member= Member(user=user)
   member.save()

class Transaction(models.Model):
   name = models.CharField(max_length=100)
   description = models.TextField()
   group = models.ForeignKey(Group)
   payer = models.ForeignKey(Member)
   amount= models.DecimalField(max_digits=8, decimal_places=2)
   date = models.DateField()

   def __unicode__(self):
      return self.name