from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Quest, Location
from .forms import SessionForm

def home(request):
    return render(request, 'home.html')

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

def quest_index(request):
    quests = Quest.objects.all()
    return render(request, 'quests/index.html', {'quests': quests})

def quest_detail(request, quest_id):
    quest = Quest.objects.get(id=quest_id)
    session_form = SessionForm()
    return render(request, 'quests/detail.html', {'quest': quest, 'session_form': session_form})

class QuestCreate(CreateView):
    model = Quest
    fields = ['title', 'region', 'description']
    success_url = '/quests/'

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
    success_url = '/toys/'