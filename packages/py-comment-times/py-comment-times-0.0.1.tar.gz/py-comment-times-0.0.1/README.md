# Basic Python Library That Gives Times Ago, Times Due Or Multiple Time Formats(Pick Any In The Array)

    ## Below is an example how you use it

    from py_comment_times import get_times_far, get_times_format
    
    import datetime
    from datetime import timezone

    now = datetime.datetime.now(timezone.utc)

    next = now + datetime.timedelta(1,3)

    print(get_times_format(next))

    print(get_times_far(next))
        