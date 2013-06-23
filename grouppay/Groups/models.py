from django.db import models

# Create your models here.
class Group(models.Model):
   name = models.CharField(max_length=100)

   def __unicode__(self):
      return self.name

class Member(models.Model):
   user = models.OneToOneField('auth.User')
   groups = models.ManyToManyField(Group, through='Group')

   def __unicode__(self):
      return self.user.get_full_name()

class Transaction(models.Model):
   name = models.CharField(max_length=100)
   description = models.TextField()
   payer = models.ForeignKey(Member)
   amount = models.FloatField()
   date = models.DateField()

   def __unicode__(self):
      return self.name