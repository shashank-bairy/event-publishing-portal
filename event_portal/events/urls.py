from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('events_home/', views.EventListView.as_view(), name='events-home'),
    path('about/', views.about, name='about'),
    path('event_detail/<int:pk>', views.EventDetailView.as_view(), name='event_detail'),
    path('create_event/', views.EventCreateView.as_view(), name='create_event'),
    path('update_event/<int:pk>', views.EventUpdateView.as_view(), name='update_event'),
    path('delete_event/<int:pk>', views.EventDeleteView.as_view(), name='delete_event'),
    path('<int:pk>/add_attendee', views.add_attendee, name='add_attendee'),
    path('<int:pk>/remove_attendee', views.remove_attendee, name='remove_attendee'),
    path('<int:event_pk>/remove_specific_attendee/<int:user_pk>', views.remove_specific_attendee, name='remove_specific_attendee'),
    path('<int:pk>/attendees_list', views.AttendeeListView.as_view(), name='attendees_list'),
    path('manage_events/', views.ManageEventsListView.as_view(), name='manage_events'),
    path('attending_events/', views.AttendingEventsListView.as_view(), name='attending_events'),
    path('', views.home, name='welcome')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
