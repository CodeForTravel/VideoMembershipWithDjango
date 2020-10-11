from django.shortcuts import render
from django.views import View

class HomeView(View):
    template_name = 'home.html'
    def get(self,request):
        args = {

        }
        return render(request,self.template_name,args)