from django.db import models
from registration.signals import user_registered
from django.contrib.auth.models import User
from django.dispatch import receiver
from groups.models import Group

class Member(models.Model):
   # Connect the member model to the user profile
   user = models.OneToOneField('auth.User')
   # Additional member attributes
   groups = models.ManyToManyField(Group)
   def __unicode__(self):
      return self.user.get_full_name()

@receiver(user_registered)
def createMember(sender, user, request, **kwargs):
   member= Member(user=user)
   member.save()


class Non_Registered_Member(models.Model):
   name = models.CharField(max_length=100)
   amount=models.DecimalField(max_digits=8, decimal_places=2)
   connection=models.ForeignKey(Member)
   groups = models.ManyToManyField(Group)

