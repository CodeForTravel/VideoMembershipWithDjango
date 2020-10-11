from django.shortcuts import render
from django.views.generic import View
from memberships.views import get_user_subscription,get_user_membership

class ProfileView(View):
    template_name = 'users/user_profile.html'
    def get(self,request):
        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)
        args = {
            'user_membership':user_membership,
            'user_subscription':user_subscription
        }
        return render(request,self.template_name,args)