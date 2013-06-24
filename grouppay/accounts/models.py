from django.db import models
from groups.models import Group, Transaction


class UserProfile(models.Model):
   # Connect the member model to the user profile
   user = models.OneToOneField('auth.User')

   # Additional member attributes
   groups = models.ManyToManyField(Group)

   def __unicode__(self):
      return self.user.get_full_name()

