from django.contrib import admin
from .models import Quest, Session, Location 
# Register your models here.

admin.site.register(Quest)
admin.site.register(Session)
admin.site.register(Location)