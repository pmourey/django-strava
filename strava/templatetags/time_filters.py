# In your app/templatetags/time_filters.py
from django import template

register = template.Library()


@register.filter
def format_duration(seconds):
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
