from django import template

register = template.Library()

@register.filter
def get_score(progress_map, lesson_id):
    progress = progress_map.get(lesson_id)
    return getattr(progress, "score", "")