from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    # Routes will be added here
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('quests/', views.quest_index, name='quest-index'),
    path('quests/<int:quest_id>/', views.quest_detail, name='quest-detail'),
    path('quests/create', views.QuestCreate.as_view(), name='quest-create'),
    path('quests/<int:pk>/update/', views.QuestUpdate.as_view(), name='quest-update'),
    path('quests/<int:pk>/delete/', views.QuestDelete.as_view(), name='quest-delete'),
    path('quests/<int:quest_id>/add-session', views.add_session, name='add-session'),
    path('locations/', views.LocationList.as_view(), name='location-index'),
    path('locations/<int:pk>/', views.LocationDetail.as_view(), name='location-detail'),
    path('locations/create/', views.LocationCreate.as_view(), name='location-create'),
    path('toys/<int:pk>/update/', views.LocationUpdate.as_view(), name='location-update'),
    path('toys/<int:pk>/delete/', views.LocationDelete.as_view(), name='location-delete'),

]

