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

]

