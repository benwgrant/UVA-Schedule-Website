from django.contrib import admin
from django.urls import include, path
from .views import index, superuser, user


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('superuser/', views.superuser, name='superuser'),
    path('user/', views.user, name='user'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    # all searchPage app specific things including
    path('searchPage', views.searchPage, name='searchPage'),
    path('displayClasses', views.displayClasses, name='displayClasses'),
    path('displaySections', views.displaySections, name='displaySections'),
    # all schedule and superuser specific things
    path('displayCart', views.displayCart, name='displayCart'),
    path('deleteClass', views.deleteClass, name='deleteClass'),
    path('displaySchedules', views.displaySchedules, name='saveCartToSchedule'),
    path('sendSchedule', views.sendSchedule, name="sendSchedule"),
    path("deleteSchedule", views.deleteSchedule, name='deleteSchedule'),
    path('generateAdvisor', views.generateAdvisor, name='generateAdvisor'),
    path('approveSchedule', views.approveSchedule, name='approveSchedule'),
    path('rejectSchedule', views.rejectSchedule, name='rejectSchedule'),
    path('chooseAdvisor', views.chooseAdvisor, name="chooseAdvisor"),
    path('convertToAdvisor', views.convertToAdvisor, name="convertToAdvisor"),
    path('convertToUser', views.convertToUser, name="convertToUser"),
]
