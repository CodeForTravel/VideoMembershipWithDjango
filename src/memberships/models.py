from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save,post_save
from datetime import datetime
import stripe
stripe.api_key = settings.STRIPE_PRIVATE_KEY


class MembershipChoice(models.TextChoices):
    ENTERPRISE = 'Enterprise', 'Enterprise'
    PROFESSIONAL = 'Professional', 'Professional'
    FREE = 'Free', 'Free'


class Membership(models.Model):
    slug            = models.SlugField()
    membership_type = models.CharField(max_length=100, choices=MembershipChoice.choices,
                                                        default=MembershipChoice.FREE)
    price           = models.FloatField(default=15)
    stripe_plan_id  = models.CharField(max_length =40)
    logo            = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.membership_type



def post_save_usermembership_create(sender,instance, created, *args, **kwargs):
    if created:
        UserMembership.objects.get_or_create(user=instance)
    
    user_membership, created = UserMembership.objects.get_or_create(user=instance)

    if user_membership.stripe_customer_id is None or user_membership.stripe_customer_id == '':
        new_stripe_customer_id = stripe.Customer.create(email =instance.email)
        user_membership.stripe_customer_id = new_stripe_customer_id['id']
        user_membership.save()
post_save.connect(post_save_usermembership_create,sender=settings.AUTH_USER_MODEL)




class UserMembership(models.Model):
    user                = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    stripe_customer_id  = models.CharField(max_length=40)
    membership          = models.ForeignKey(Membership,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.user.username


class Subscription(models.Model):
    user_membership         = models.ForeignKey(UserMembership, on_delete=models.CASCADE)
    stripe_subscriptions_id = models.CharField(max_length=50)
    active                  = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user_membership.user.username

    @property
    def get_created_date(self):
        sub = stripe.Subscription.retrieve(self.stripe_subscriptions_id)
        return datetime.fromtimestamp(sub.created)

    @property
    def get_next_billing_date(self):
        sub = stripe.Subscription.retrieve(self.stripe_subscriptions_id)
        return datetime.fromtimestamp(sub.current_period_end)


