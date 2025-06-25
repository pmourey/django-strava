import os
from pathlib import Path
from gpxpy import parse
import locale
from pytz import timezone

def get_strava_path():
	base_path = Path(__file__).parent
	gpx_dir = base_path / 'gpx_files'

	# Create directory if it doesn't exist
	gpx_dir.mkdir(parents=True, exist_ok=True)

	return str(gpx_dir)


def get_activities() -> list[tuple]:
	gpx_strava_path = get_strava_path()
	activities: list = []
	for filename in sorted(os.listdir(gpx_strava_path)):
		if filename.endswith('.gpx'):
			# print("-" * 80)
			with open(f'{gpx_strava_path}/{filename}', 'r') as gpx_file:
				gpx: GPX = parse(gpx_file)
				moving_data: MovingData = gpx.get_moving_data()

				# Try to get activity type from different possible locations
				activity_type = None
				if gpx.tracks and gpx.tracks[0].type:
					activity_type = gpx.tracks[0].type
				elif gpx.tracks and hasattr(gpx.tracks[0], 'extensions'):
					# Try to find activity type in extensions
					for ext in gpx.tracks[0].extensions:
						if 'type' in str(ext).lower():
							activity_type = ext.text
							break

				# Default to 'unknown' if no type found
				activity_type = activity_type or 'unknown'

				locale.setlocale(locale.LC_TIME, 'fr_FR')
				start_time = gpx.get_time_bounds().start_time.astimezone(timezone('Europe/Paris'))
				end_time = gpx.get_time_bounds().end_time.astimezone(timezone('Europe/Paris'))
				day, hour = start_time.strftime('%A %d %B %Y'), start_time.strftime('%Hh%M')
				elapsed_time = gpx.get_duration()
				distance3d = gpx.length_3d() / 1000
				max_speed_kmh = moving_data.max_speed * 3600 / 1000
				average_speed_kmh = moving_data.moving_distance / (1000 * moving_data.moving_time / 3600)
				activity_label: str = filename.split('.')[0]
				elapsed_hours, elapsed_minutes = divmod(elapsed_time / 60, 60)
				duration: str = f'{int(elapsed_hours)}h {round(elapsed_minutes)}\''
				# activities.append((day, hour, distance3d, duration, average_speed_kmh, max_speed_kmh, activity_label))
				activities.append((start_time, distance3d, elapsed_time, average_speed_kmh, max_speed_kmh, activity_label, activity_type))
	return sorted(activities, key=lambda x: x[0], reverse=True)  # newest first

