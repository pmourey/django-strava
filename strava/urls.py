from django.urls import path, include
from . import views

app_name = 'strava'

urlpatterns = [
	# path('', views.accueil, name='accueil'), # enable this to restore default behavior (using GPX parsing)
	path('activities/', views.activity_list, name='activity_list'),
	# path('', views.base_map, name='Base Map View'),
	path('', views.index, name='index'), # replaced by connected/ url
	path('connected/', views.connected_map, name='Connect Map View'),
	path("oauth/", include("social_django.urls", namespace="social")),
	# path('social-auth/', include('social_django.urls', namespace='social')),
]
