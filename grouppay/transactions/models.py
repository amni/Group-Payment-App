from django.db import models
from groups.models import Group
from members.models import Non_Registered_Member

# Create your models here.
class Transaction(models.Model):
   name = models.CharField(max_length=100)
   description = models.TextField()
   group= models.ForeignKey(Group, blank=True, null=True)
   friend= models.ForeignKey(Non_Registered_Member, null=True)
   amount= models.DecimalField(max_digits=8, decimal_places=2)
   date = models.DateField()

   def __unicode__(self):
      return self.name

