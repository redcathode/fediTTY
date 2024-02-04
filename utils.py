def format_seconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    
    formatted_time = ""
    if days > 0:
        formatted_time += f"{days} day{'s' if days > 1 else ''}, "
    if hours > 0:
        formatted_time += f"{hours} hour{'s' if hours > 1 else ''}, "
    if minutes > 0:
        formatted_time += f"{minutes} minute{'s' if minutes > 1 else ''}, "
    if seconds > 0:
        formatted_time += f"{seconds} second{'s' if seconds > 1 else ''}"
    
    return formatted_time.strip(', ')