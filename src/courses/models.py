from django.db import models
from memberships.models import Membership
from django.urls import reverse
from django.shortcuts import redirect

class Course(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(null=True,blank=True)
    allowed_memberships = models.ManyToManyField(Membership)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'slug': self.slug})

    @property
    def get_lessons(self):
        return self.lesson_set.all().order_by('position')
    
class Lesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL,null=True)
    video_url = models.CharField(max_length=200)
    position = models.IntegerField()
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:lesson_detail', 
        kwargs = {
            'course_slug':self.course.slug ,
            'lesson_slug':self.slug
            })