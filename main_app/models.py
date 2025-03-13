from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


# +++++++++++++++++++++ Choice Tuples +++++++++++++++++++++

SESSION_TYPES = (
    ('0', 'Dungeon Crawl'),
    ('1', 'Mystery Investigation'),
    ('2', 'Monster Hunt'),
    ('3', 'Political Intrigue'),
    ('4', 'Exploration Quest'),
    ('5', 'Heist Mission'),
    ('6', 'Rescue Operation'),
    ('7', 'Escort Duty'),
    ('8', 'Survival Challenge'),
    ('9', 'War Campaign'),
    ('10', 'Siege Defense'),
    ('11', 'Assassination Plot'),
    ('12', 'Artifact Recovery'),
    ('13', 'Arena Combat'),
    ('14', 'Rogues Gambit'),
    ('15', 'Fey Bargain'),
    ('16', 'Plague Outbreak'),
    ('17', 'Time Loop'),
    ('18', 'Underworld Dealings'),
    ('19', 'Divine Trial'),
)

LOCALES = (
    ('0', 'a Village'),
    ('1', 'a Castle'),
    ('2', 'a Hamlet'),
    ('3', 'a Town'),
    ('4', 'a City'),
    ('5', 'a Fortress'),
    ('6', 'a Keep'),
    ('7', 'a Citadel'),
    ('8', 'a Tower'),
    ('9', 'Ruins'),
    ('10', 'a Monastery'),
    ('11', 'a Temple'),
    ('12', 'a Sanctuary'),
    ('13', 'an Academy'),
    ('14', 'a Library'),
    ('15', 'a Market'),
    ('16', 'a Harbor'),
    ('17', 'an Inn'),
    ('18', 'a Mine'),
    ('19', 'a Cavern'),
    ('20', 'a Dungeon'),
    ('21', 'a Swamp'),
    ('22', 'a Forest'),
    ('23', 'a Glade'),
    ('24', 'a Meadow'),
    ('25', 'a Mountain'),
    ('26', 'a Valley'),
    ('27', 'a Desert'),
    ('28', 'a Tundra'),
    ('29', 'an Isle'),
    ('30', 'an Archipelago'),
    ('31', 'a Crypt'),
    ('32', 'Catacombs'),
)

NPC_TYPES = (
    ('0', 'Innkeeper'),
    ('1', 'Merchant'),
    ('2', 'Blacksmith'),
    ('3', 'Guard'),
    ('4', 'Noble'),
    ('5', 'Peasant'),
    ('6', 'Bounty Hunter'),
    ('7', 'Bandit'),
    ('8', 'Alchemist'),
    ('9', 'Healer'),
    ('10', 'Priest'),
    ('11', 'Cultist'),
    ('12', 'Wizard'),
    ('13', 'Sorcerer'),
    ('14', 'Druid'),
    ('15', 'Bard'),
    ('16', 'Rogue'),
    ('17', 'Ranger'),
    ('18', 'Knight'),
    ('19', 'Paladin'),
    ('20', 'Warlock'),
    ('21', 'Necromancer'),
    ('22', 'Scholar'),
    ('23', 'Sailor'),
    ('24', 'Pirate'),
    ('25', 'Hunter'),
    ('26', 'Farmer'),
    ('27', 'Fisherman'),
    ('28', 'Stablemaster'),
    ('29', 'Mayor'),
    ('30', 'King'),
    ('31', 'Queen'),
    ('32', 'Prince'),
    ('33', 'Princess'),
    ('34', 'General'),
    ('35', 'Captain'),
    ('36', 'Spy'),
    ('37', 'Beggar'),
    ('38', 'Minstrel'),
    ('39', 'Hermit'),
    ('40', 'Gladiator'),
    ('41', 'Executioner'),
    ('42', 'Gravekeeper'),
    ('43', 'Smuggler'),
    ('44', 'Assassin'),
    ('45', 'Seer'),
    ('46', 'Chieftain'),
    ('47', 'Beastmaster'),
    ('48', 'Tavern Wench'),
    ('49', 'Messenger'),
)




# +++++++++++++++++++++ Models +++++++++++++++++++++

class Location(models.Model):
    name = models.CharField(max_length=100)
    population = models.IntegerField(validators=[MaxValueValidator(1000)])
    location_type = models.CharField(max_length = 2, choices = LOCALES, default = LOCALES[0][0])
    description = models.TextField(max_length=500)
    is_visited = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} is {self.get_location_type_display()} with {self.population} souls residing there."

    def clean(self):
        # Ensure location_type is a valid choice
        valid_choices = [choice[0] for choice in LOCALES]  # Extract valid keys
        if self.location_type not in valid_choices:
            raise ValidationError({'settlement_type': 'Invalid settlement type.'})
    
    def get_absolute_url(self):
        return reverse('location-detail', kwargs={'pk': self.id})

class Quest(models.Model):
    title = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    is_complete = models.BooleanField(default=False)
    locations = models.ManyToManyField(Location)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # new code below
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('quest-detail', kwargs={'quest_id': self.id})


class NPC(models.Model):
    name = models.CharField(max_length=100)
    hitpoints = models.IntegerField(validators=[MaxValueValidator(500)])
    armor_class = models.IntegerField(validators=[MaxValueValidator(20)])
    backstory = models.TextField(max_length=500)
    npc_type = models.CharField(max_length=2, choices=NPC_TYPES, default=NPC_TYPES[0][0])
    is_alive = models.BooleanField(default=True)
    
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_npc_type_display()} named {self.name} with {self.hitpoints} hitpoints and {self.armor_class} armor class."
    
    def clean(self):
        # Ensure location_type is a valid choice
        valid_choices = [choice[0] for choice in NPC_TYPES]  # Extract valid keys
        if self.npc_type not in valid_choices:
            raise ValidationError({'npc_type': 'Invalid npc type.'})



class Session(models.Model):
    date = models.DateField()
    session_type = models.CharField(
        max_length=2,
        # add the 'choices' field option
        choices=SESSION_TYPES,
        # set the default value for meal to be 'B'
        default=SESSION_TYPES[0][0]
    )
    
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_session_type_display()} on {self.date}"
    
    def clean(self):
        # Ensure location_type is a valid choice
        valid_choices = [choice[0] for choice in SESSION_TYPES]  # Extract valid keys
        if self.session_type not in valid_choices:
            raise ValidationError({'session_type': 'Invalid session type.'})
    
    class Meta:
        ordering = ['-date']