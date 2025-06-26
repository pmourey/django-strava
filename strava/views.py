from django.shortcuts import render
from .common import get_activities
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from strava_project.decorators import group_required

import folium

import pandas as pd
import requests
import polyline


# Create your views here.

@login_required
# @group_required(['strava', 'admin'])
def accueil(request):
	return render(request, 'strava/accueil.html')


@login_required
# @group_required(['strava', 'admin'])
def index(request):
	return render(request, 'strava/index.html')


@login_required
# @group_required(['strava', 'admin'])
def activity_list(request):
	activity_filter = 'running'  # ['running', 'cycling', 'walking']
	activities = get_activities()
	activities = list(filter(lambda x: x[6] == activity_filter, activities))
	total_distance = sum(activity[1] for activity in activities)
	elapsed_time = timedelta(seconds=sum(activity[2] for activity in activities))
	average_speed = total_distance / elapsed_time.total_seconds() * 3600
	return render(request, "strava/activity_list.html", {"activities": activities, "total_distance": total_distance, "elapsed_time": elapsed_time, "average_speed": average_speed, "activity_filter": activity_filter})


@login_required
# @group_required(['strava', 'admin'])
def base_map(request):
	# Make your map object
	nantes = [47.218371, -1.553621]  # Nantes coordinates
	saint_laurent_du_var = [43.666672, 7.18333]  # Saint-Laurent-du-Var coordinates
	main_map = folium.Map(location=saint_laurent_du_var, zoom_start=12)  # Create base map
	main_map_html = main_map._repr_html_()  # Get HTML for website

	context = {"main_map": main_map_html}
	return render(request, 'strava/index.html', context)


@login_required
# @group_required(['strava', 'admin'])
def connected_map(request):
	# Make your map object
	nantes = [47.218371, -1.553621]  # Nantes coordinates
	saint_laurent_du_var = [43.666672, 7.18333]  # Saint-Laurent-du-Var coordinates
	main_map = folium.Map(location=saint_laurent_du_var, zoom_start=12)  # Create base map
	user = request.user  # Pulls in the Strava User data
	strava_login = user.social_auth.get(provider='strava')  # Strava login
	access_token = strava_login.extra_data['access_token']  # Strava Access token
	activites_url = "https://www.strava.com/api/v3/athlete/activities"

	# Get activity data
	header = {'Authorization': 'Bearer ' + str(access_token)}
	activity_df_list = []
	for n in range(5):  # Change this to be higher if you have more than 1000 activities
		param = {'per_page': 200, 'page': n + 1}

		activities_json = requests.get(activites_url, headers=header, params=param).json()
		if not activities_json:
			break
		activity_df_list.append(pd.json_normalize(activities_json))

	# Get Polyline Data
	activities_df = pd.concat(activity_df_list)
	activities_df = activities_df.dropna(subset=['map.summary_polyline'])
	activities_df['polylines'] = activities_df['map.summary_polyline'].apply(polyline.decode)

	# Plot Polylines onto Folium Map
	for pl in activities_df['polylines']:
		if len(pl) > 0:  # Ignore poly lines with length zero (Thanks @Joukesmink for the tip)
			folium.PolyLine(locations=pl, color='red').add_to(main_map)

	# Return HTML version of map
	main_map_html = main_map._repr_html_()  # Get HTML for website
	context = {"main_map": main_map_html}
	return render(request, 'strava/index.html', context)
