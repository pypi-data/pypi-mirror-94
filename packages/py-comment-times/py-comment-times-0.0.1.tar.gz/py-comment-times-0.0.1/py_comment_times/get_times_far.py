import datetime
from datetime import timezone

def check_positive(number):
    if number > 0:
        return "ago"
    elif number < 0:
        return "due"
    else: 
        return "right now"

def get_times_far(timestamp):
    posted = timestamp
    now = datetime.datetime.now(timezone.utc)
    x = now.date()-posted.date()
    time = ""
    if x.days > 0 or x.days < 0:
        if x.days > 1 or x.days < -1:
            time = f"{abs(x.days)} days"
        else:
            time = f"{abs(x.days)} day"
        time = {
            "time": time,
            "away": check_positive(x.days)
        }       
    else:
        seconds = (now-posted).total_seconds()
        real_number = seconds
        seconds = round(abs(seconds))
        print(seconds)
        if seconds > 60:
            minutes = round(seconds/60)
            print(minutes)
            if minutes > 60:
                hours = round(minutes/60)
                if hours > 1:
                    time = f"{abs(hours)} hours"
                else:
                    time = f"{abs(hours)} hour"
            else:
                if minutes > 1:
                    time = f"{abs(minutes)} minutes"
                else:
                    time = f"{abs(minutes)} minute"
        else:
            if seconds > 1:
                time = f"{abs(seconds)} seconds"
            else:
                time = f"1 second"
        time = {
            "time": time,
            "away": check_positive(real_number)
        }
    return time