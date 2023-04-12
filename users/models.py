from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    person_age = models.FloatField(default=0)
    person_income = models.FloatField(default=0)
    person_home_ownership = models.CharField(max_length=8, blank=True)
    person_emp_length = models.FloatField(default=0)
    loan_intent = models.CharField(max_length=17, blank=True)
    loan_grade = models.CharField(max_length=1, blank=True)

    loan_amnt = models.FloatField(default=0)
    loan_int_rate = models.FloatField(default=0)
    loan_percent_income = models.FloatField(default=0)
    cb_person_default_on_file = models.BooleanField(default=False)
    cb_person_cred_hist_length = models.FloatField(default=0)

    liquid_funds = models.FloatField(default=0)
    is_borrower = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    # if created:
    #     Profile.objects.create(user=instance)
    # instance.profile.save()

    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)
