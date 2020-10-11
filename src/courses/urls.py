from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('course_list/',views.CourseView.as_view(), name='course_list'),
    path('course_detail/<slug>/',views.CourseDetailView.as_view(), name='course_detail'),
    path('lesson_detail/<course_slug>/<lesson_slug>/',views.LessonDetailView.as_view(), name='lesson_detail'),
]
