from datetime import datetime
from dateutil.relativedelta import relativedelta


def formatted_string(value: str):
    return " ".join(value.split("_")).title()


def time_difference(created_at, due_date):
    now = datetime.now()
    difference = due_date - now
    
    if difference.total_seconds() < 0:
        return "Past due"
    elif difference.total_seconds() < 60:
        return "Less than a minute left"
    elif difference.total_seconds() < 3600:
        minutes = int(difference.total_seconds() // 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} left"
    elif difference.total_seconds() < 86400:
        hours = int(difference.total_seconds() // 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} left"
    else:
        delta = relativedelta(due_date, now)
        if delta.years > 0:
            return f"{delta.years} year{'s' if delta.years > 1 else ''} left"
        elif delta.months > 0:
            return f"{delta.months} month{'s' if delta.months > 1 else ''} left"
        elif delta.days >= 7:
            weeks = delta.days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''} left"
        else:
            return f"{delta.days} day{'s' if delta.days > 1 else ''} left"