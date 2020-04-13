from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import UpdateView
from .models import Event
from .forms import EventForm

# Create your views here.
def home(request):
  if request.user.is_authenticated:
    return redirect('/events_home')    
  return render(request, 'events/index.html')

def about(request):
  return render(request, 'events/about.html')  


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/create_event.html'
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.organizer = self.request.user
        self.object.save()
        return redirect('/')

    def get_context_data(self, **kwargs):
      context = super(EventCreateView, self).get_context_data(**kwargs)
      context['creation'] = True
      return context

class EventListView(LoginRequiredMixin, ListView):
    template_name = 'events/events_home.html'
    model = Event
    queryset = Event.objects.all()
    context_object_name = 'events'
    ordering = ['date']

class EventDetailView(LoginRequiredMixin, DetailView):
    template_name = 'events/event_detail.html'
    model = Event
    queryset = Event.objects.all()
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
      context = super(EventDetailView, self).get_context_data(**kwargs)
      user = self.request.user
      event = self.object
      if event.attendees.filter(id = user.id).exists():
        context['is_attending'] = True
      return context

class EventUpdateView(LoginRequiredMixin,UpdateView):
    template_name = 'events/create_event.html'
    model = Event
    form_class = EventForm

    def form_valid(self, form):
      event = form.save(commit=False)
      event.save()
      return redirect('/')

class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = '/'

class ManageEventsListView(LoginRequiredMixin, ListView):
    template_name = 'events/manage_events.html'
    model = Event
    context_object_name = 'events'
    ordering = ['date']

    def get_queryset(self):
      return Event.objects.filter(organizer=self.request.user)

class AttendingEventsListView(LoginRequiredMixin, ListView):
    template_name = 'events/attending_events_list.html'
    model = Event
    context_object_name = 'events'
    ordering = ['date']

    def get_queryset(self):
      return Event.objects.filter(attendees=self.request.user)


class AttendeeListView(ListView):
    template_name = 'events/attendees_list.html'
    model = User
    context_object_name = 'attendees'

    def get_queryset(self):
      return Event.objects.get(pk=self.kwargs['pk']).attendees.all()

    def get_context_data(self, **kwargs):
      context = super(AttendeeListView, self).get_context_data(**kwargs)
      context['event'] = Event.objects.get(pk=self.kwargs['pk'])
      return context

@login_required
def add_attendee(request, pk):
    user = request.user
    event = Event.objects.get(pk = pk)
    event.attendees.add(user)
    return redirect(f'/event_detail/{pk}')

@login_required
def remove_attendee(request, pk):
    user = request.user
    event = Event.objects.get(pk = pk)
    event.attendees.remove(user)
    return redirect(f'/event_detail/{pk}')

@login_required
def remove_specific_attendee(request, event_pk ,user_pk):
    user = User.objects.get(pk=user_pk)
    event = Event.objects.get(pk = event_pk)
    event.attendees.remove(user)
    return redirect(f'/{event_pk}/attendees_list')