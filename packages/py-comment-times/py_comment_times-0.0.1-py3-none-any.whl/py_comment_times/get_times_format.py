import datetime

def get_format_1(timestamp):
    day = timestamp.strftime("%d")
    month = timestamp.strftime("%B")
    year = timestamp.strftime("%Y")
    return f"{day} {month},{year}"

def get_format_2(timestamp):
    day = timestamp.strftime("%d")
    month = timestamp.strftime("%m")
    year = timestamp.strftime("%Y")
    return f"{day}-{month}-{year}"

def get_format_3(timestamp):
    day = timestamp.strftime("%d")
    month = timestamp.strftime("%m")
    year = timestamp.strftime("%Y")
    return f"{month}-{day}-{year}"

def get_format_4(timestamp):
    day = timestamp.strftime("%d")
    month = timestamp.strftime("%m")
    year = timestamp.strftime("%Y")
    return f"{year}-{month}-{day}"

def get_times_format(timestamp):

    return [get_format_1(timestamp), get_format_2(timestamp), get_format_3(timestamp), get_format_4(timestamp)]