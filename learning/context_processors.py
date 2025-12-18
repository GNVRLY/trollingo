def xp_context(request):
    if not request.user.is_authenticated:
        return {}

    profile = getattr(request.user, "profile", None)

    xp_total = getattr(profile, "xp", 0) if profile else 0
    xp_level = getattr(profile, "level", 1) if profile else 1
    xp_in_level = getattr(profile, "xp_in_level", xp_total % 100) if profile else (xp_total % 100)
    xp_to_next = getattr(profile, "xp_to_next_level", 100 - xp_in_level) if profile else (100 - xp_in_level)
    xp_percent = getattr(profile, "xp_progress_percent", xp_in_level) if profile else xp_in_level

    try:
        xp_percent = int(xp_percent)
    except Exception:
        xp_percent = 0
    xp_percent = max(0, min(100, xp_percent))

    return {
        "xp_level": xp_level,
        "xp_total": xp_total,
        "xp_in_level": xp_in_level,
        "xp_to_next": xp_to_next,
        "xp_percent": xp_percent,
    }
