from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

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

