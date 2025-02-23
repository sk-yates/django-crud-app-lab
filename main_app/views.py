from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Quest, Location
from .forms import SessionForm

# def home(request):
#     return render(request, 'home.html')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('cat-index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
    # Same as: 
    # return render(
    #     request, 
    #     'signup.html',
    #     {'form': form, 'error_message': error_message}
    # )


class Home(LoginView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html')

def quest_index(request):
    return render(request, 'quests/index.html', {'quests': sample_quests})

class Sample_quest:
    def __init__(self, title, region, description):
        self.title = title
        self.region = region
        self.description = description
        self.is_complete = False

sample_quests = [
    Sample_quest('Sleepless Knights', 'Waterdeep', 'The knights of Waterdeep have haunted dreams!'),
    Sample_quest('The Bloody Well', 'Dagger Ford', 'The drinking water of the town has been contaminated!'),
    Sample_quest('The Grateful Gurdy Player ', 'Neverwinter', 'The hurdy gurdy player has a quest for you, adventurers!'),
    Sample_quest('The Wailing Shack', 'Icewind Dale', 'The local Whaler is being haunter by a Banshee!')
]

@login_required
def quest_index(request):
    # quests = Quest.objects.all()
    quests = Quest.objects.filter(user=request.user)
    return render(request, 'quests/index.html', {'quests': quests})

@login_required
def quest_detail(request, quest_id):
    quest = Quest.objects.get(id=quest_id)
    # locations = Location.objects.all()
    locations_available = Location.objects.exclude(id__in = quest.locations.all().values_list('id'))
    session_form = SessionForm()
    return render(request, 'quests/detail.html', {'quest': quest, 'session_form': session_form, 'locations': locations_available})

class QuestCreate(LoginRequiredMixin, CreateView):
    model = Quest
    fields = ['title', 'region', 'description']
    # success_url = '/quests/'
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the cat
        # Let the CreateView do its job as usual
        return super().form_valid(form)

class QuestUpdate(UpdateView):
    model = Quest
    fields = ['title', 'region', 'description']

class QuestDelete(DeleteView):
    model = Quest
    success_url = '/quests/'


def add_session(request, quest_id):
    form = SessionForm(request.POST)
    if form.is_valid():
        new_session = form.save(commit=False)
        new_session.quest_id = quest_id
        new_session.save()
    return redirect('quest-detail', quest_id=quest_id)

class LocationCreate(CreateView):
    model = Location
    fields = '__all__'

class LocationList(ListView):
    model = Location

class LocationDetail(DetailView):
    model = Location

class LocationUpdate(UpdateView):
    model = Location
    fields = ['name', 'color']

class LocationDelete(DeleteView):
    model = Location
    success_url = '/quests/'

def associate_location(request, quest_id, location_id):
    Quest.objects.get(id=quest_id).locations.add(location_id)
    return redirect('quest-detail', quest_id=quest_id)

def remove_location(request, quest_id, location_id):
    quest, location = Quest.objects.get(id=quest_id), Location.objects.get(id=location_id)
    quest.locations.remove(location)
    return redirect('quest-detail', quest_id=quest_id)