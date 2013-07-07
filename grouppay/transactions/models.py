from django.db import models
from groups.models import Group
from members.models import Non_Registered_Member

# Create your models here.
class IndividualTransaction(models.Model):
   name = models.CharField(max_length=100)
   description = models.TextField()
   amount= models.DecimalField(max_digits=8, decimal_places=2)
   date = models.DateField()

   def __unicode__(self):
      return self.names

class GroupTransaction(models.Model):
   name = models.CharField(max_length=100)
   description = models.TextField()
   group = models.ForeignKey(Group)
   amount= models.DecimalField(max_digits=8, decimal_places=2)
   date = models.DateField()

