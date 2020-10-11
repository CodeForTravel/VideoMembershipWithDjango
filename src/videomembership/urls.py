
from django.contrib import admin
from django.urls import path,include
from . import views


'''______ for image file_____'''
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.HomeView.as_view(),name='home'),
    path('users/', include('users.urls',namespace='users')),
    path('memberships/', include('memberships.urls',namespace='memberships')),
    path('courses/', include('courses.urls',namespace='courses')),

]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
