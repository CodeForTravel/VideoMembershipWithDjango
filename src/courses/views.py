from django.shortcuts import render
from django.views.generic import DetailView,ListView,View
from courses.models import Course
from memberships.models import UserMembership

class CourseView(View):
    template_name = 'courses/course_list.html'
    def get(self,request):
        courses = Course.objects.all()
        args = {
            'courses':courses
        }
        return render(request, self.template_name,args)



class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'


class LessonDetailView(View):
    template_name = 'courses/lesson_detail.html'
    def get(self,request, course_slug,lesson_slug,*args,**kwargs):

        course_qs = Course.objects.filter(slug=course_slug)
        if course_qs.exists():
            course = course_qs[0]

        lesson_qs = course.get_lessons.filter(slug=lesson_slug)
        if lesson_qs.exists():
            lesson = lesson_qs.first()
        
        user_membership = UserMembership.objects.filter(user=request.user).first()
        user_membership_type = user_membership.membership.membership_type
        course_allowed_membership_types = course.allowed_memberships.all()
        args = {
            'lesson':None
        }
        if course_allowed_membership_types.filter(membership_type=user_membership_type).exists():
            args = { 'lesson':lesson }
        return render(request, self.template_name,args)
