from django.shortcuts import render,redirect
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View

from .models import Membership,UserMembership,Subscription
import stripe



def get_user_subscription(request):
    user_subscription_qs = Subscription.objects.filter(
        user_membership = get_user_membership(request)
    )
    if user_subscription_qs.exists():
        return user_subscription_qs.first()
    return None

def get_selected_membership_obj(selected_membership_type):
    selected_membership_qs = Membership.objects.filter(
                     membership_type = selected_membership_type)
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None

def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None


class MembershipSelectView(View):
    template_name = 'memberships/membership_select.html'
    def get(self,request):
        object_list = Membership.objects.all()
        current_user_membership = get_user_membership(request)

        args = {
            'object_list':object_list,
            'current_user_membership':str(current_user_membership.membership)
        }
        return render(request,self.template_name,args)
    def post(self,request,**kwargs):
        selected_membership_type = request.POST.get('membership_type')
        current_user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)

        selected_membership_obj = get_selected_membership_obj(selected_membership_type)

        # VALIDATIONS ==============

        if current_user_membership.membership == selected_membership_obj:
            if user_subscription != None:
                messages.info(request,"You already have this membership! your \
                    next payment is due{}".format('get this value from stripe '))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # ASSIGN TO THE SESSION
        request.session['selected_membership_type'] = selected_membership_obj.membership_type

        args = {
        }
        return HttpResponseRedirect(reverse('memberships:payment'))




def PaymentView(request):
    template_name = 'memberships/membership_payment.html'
    membership_type = request.session['selected_membership_type']
    selected_membership_obj = get_selected_membership_obj(membership_type)
    user_membership = get_user_membership(request)
    
    publishKey = settings.STRIPE_PUBLIC_KEY
    
    if request.method == "POST":
        try:
            token = request.POST['stripeToken']
            cus = stripe.Customer.retrieve(user_membership.stripe_customer_id)
            cus.source = token
            cus.save()
            subscription = stripe.Subscription.create(
                customer=user_membership.stripe_customer_id,
                items=[{
                    'plan': selected_membership_obj.stripe_plan_id
                }]
            )
            return redirect(reverse('memberships:update_transactions', kwargs={
                'sub_id': subscription.id
            }))
        except stripe.error.CardError:
            messages.info(request, 'Your card has been declined')

    args ={
        'publishKey': publishKey,
        'selected_membership_obj': selected_membership_obj
    }
    return render(request, template_name,args)

class UpdateTransactionView(View):
    def get(self,request,sub_id):
        membership_type = request.session['selected_membership_type']
        selected_membership_obj = get_selected_membership_obj(membership_type)
        user_membership = get_user_membership(request)
        user_membership.membership = selected_membership_obj
        user_membership.save()
        sub ,created = Subscription.objects.get_or_create(user_membership=user_membership)
        sub.stripe_subscriptions_id = sub_id
        sub.active = True
        sub.save()
        try:
            del request.session['selected_membership_type']
        except:
            pass
        messages.info(request, 'Successfully created {} membership!'.format(selected_membership_obj))
        args = {

        }
        return redirect('courses:course_list')

class CancelSubscription(View):
    def get(self,request):
        user_subscription = get_user_subscription(request)
        if user_subscription.active == False:
            messages.info(request,"You don't have an active membership!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        sub = stripe.Subscription.retrieve(user_subscription.stripe_subscriptions_id)
        sub.delete()
        user_subscription.active = False
        user_subscription.save()
        free_membership = Membership.objects.filter(membership_type='Free').first()
        user_membership = get_user_membership(request)
        user_membership.membership = free_membership
        user_membership.save()
        messages.info(request,"Successfully Cancelled Membership!, We have sent an email")
        #Sent An Email

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        
