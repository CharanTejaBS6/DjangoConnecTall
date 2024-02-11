from django.urls import path
from . import views
from .views import leaderboard

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('home/', views.home,  name='home'), 
    path('logout/', views.logout, name='logout'),
    path('calendar/', views.calendar, name='calendar'),
    path('add/', views.add_event, name='add_event'),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('interest/<int:event_id>/', views.show_interest, name='show_interest'),
    path('add_event_login/', views.add_event_login, name='add_event_login'),
    path('raise_hand/', views.raise_hand, name='raise_hand'),
    path('raised_hands/', views.raised_hands, name='raised_hands'),
    path('recent-events/', views.recent_events, name='recent_events'),
    path('register/<int:event_id>/', views.register_for_event, name='register_for_event'),
    path('success/', views.success_page, name='success_page'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('comment_page/', views.comment_page, name='comment_page'),
]
