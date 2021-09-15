from .models import UserAccount,UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=UserAccount) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
   
@receiver(post_save, sender=UserAccount) 
def save_profile(sender, instance, **kwargs):
        instance.userprofile.save()