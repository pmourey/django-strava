# In your app/templatetags/time_filters.py
from django import template
from django.utils.dateparse import parse_datetime
from datetime import datetime
import locale

register = template.Library()


@register.filter(name='format_strava_date')
def format_strava_date_old(value):
    if not value:
        return ''
    if isinstance(value, str):
        parsed_date = parse_datetime(value)
        if parsed_date:
            return parsed_date.strftime('%d/%m/%Y à %Hh%M')
    return value


@register.filter(name='format_strava_date')
def format_strava_date(value):
	if not value:
		return ''

	# Configurer la locale en français
	try:
		locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
	except:
		try:
			locale.setlocale(locale.LC_TIME, 'fr_FR')
		except:
			pass

	if isinstance(value, str):
		parsed_date = parse_datetime(value)
		if parsed_date:
			# %A pour le jour de la semaine complet
			return parsed_date.strftime('%A %d/%m/%Y à %Hh%M')
	return value

@register.filter
def to_km(value):
    try:
        return float(value) / 1000
    except (ValueError, TypeError):
        return 0


@register.filter(name='to_kmh')
def to_kmh(value):
    try:
        return float(value) * 3.6  # convertit m/s en km/h
    except (ValueError, TypeError):
        return 0

@register.filter
def format_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours}h{minutes:02d}m{seconds:02d}s"

@register.filter
def format_duration_old(seconds):
	hours = int(seconds // 3600)
	minutes = int((seconds % 3600) // 60)
	seconds = int(seconds % 60)

	if hours > 0:
		return f"{hours:01d}:{minutes:02d}:{seconds:02d}"
	else:
		return f"{minutes:02d}:{seconds:02d}"


@register.filter
def format_duration_text(seconds):
	hours = seconds // 3600
	minutes = (seconds % 3600) // 60
	seconds = seconds % 60

	parts = []
	if hours > 0:
		parts.append(f"{hours}h")
	if minutes > 0:
		parts.append(f"{minutes}m")
	if seconds > 0 or not parts:  # include seconds if it's the only non-zero value
		parts.append(f"{seconds}s")

	return " ".join(parts)
