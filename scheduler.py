import datetime
import time
import schedule

import database
from social_networks import facebook, twitter, instagram

current_daily_tasks = []
current_weekly_tasks = []
current_monthly_tasks = []
current_custom_tasks = []

date = datetime.date.today()


# ---------------- schedule -------------------- #

def do_schedule():
    global current_daily_tasks
    global current_weekly_tasks
    global current_monthly_tasks
    global  current_custom_tasks

    current_daily_tasks = database.get_today_daily_tasks(
        get_current_dateISOformat()
    )
    current_weekly_tasks = database.get_today_weekly_tasks(
        get_current_dateISOformat(),
        get_current_weekday_string()
    )
    current_monthly_tasks = database.get_today_monthly_tasks(
        get_current_dateISOformat(),
        get_current_day_int(),
        get_current_month_string()
    )
    current_custom_tasks = database.get_today_custom_tasks(
        get_current_dateISOformat(),
        get_current_weekday_string(),
        get_current_month_string()
    )

    print(current_daily_tasks)

    schedule.every(10).seconds.do(check_tasks)
    while True:
        schedule.run_pending()
        time.sleep(1)


def check_tasks():
    global current_daily_tasks
    global current_weekly_tasks
    global current_monthly_tasks
    global current_custom_tasks
    global date

    current_date = datetime.date.today()
    if date != current_date:
        date = current_date

        # reloading of the tasks
        current_daily_tasks = database.get_today_daily_tasks(
            get_current_dateISOformat()
        )

        current_weekly_tasks = database.get_today_weekly_tasks(
            get_current_dateISOformat(),
            get_current_weekday_string()
        )

        current_monthly_tasks = database.get_today_monthly_tasks(
            get_current_dateISOformat(),
            get_current_day_int(),
            get_current_month_string()
        )

        current_custom_tasks = database.get_today_custom_tasks(
            get_current_dateISOformat(),
            get_current_weekday_string(),
            get_current_month_string()
        )

    do_tasks()


def do_tasks():
    global current_daily_tasks
    global current_weekly_tasks
    global current_monthly_tasks
    global current_custom_tasks

    for task in current_daily_tasks:
        if task["social_network"] == "facebook":
            facebook.share_to_fb(task)
        if task["social_network"] == "instagram":
            instagram.share_to_instagram(task)
        if task["social_network"] == "twitter":
            twitter.share_to_twitter(task)

    for task in current_weekly_tasks:
        if task["social_network"] == "facebook":
            facebook.share_to_fb(task)
        if task["social_network"] == "instagram":
            instagram.share_to_instagram(task)
        if task["social_network"] == "twitter":
            twitter.share_to_twitter(task)

    for task in current_monthly_tasks:
        if task["social_network"] == "facebook":
            facebook.share_to_fb(task)
        if task["social_network"] == "instagram":
            instagram.share_to_instagram(task)
        if task["social_network"] == "twitter":
            twitter.share_to_twitter(task)

    for task in current_custom_tasks:
        if task["social_network"] == "facebook":
            facebook.share_to_fb(task)
        if task["social_network"] == "instagram":
            instagram.share_to_instagram(task)
        if task["social_network"] == "twitter":
            twitter.share_to_twitter(task)

# ---------------- helpers -------------------- #


def get_current_weekday_string():
    days = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]
    return days[datetime.date.today().weekday()]


def get_current_month_string():
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    return months[datetime.date.today().month - 1]


def get_current_dateISOformat():
    return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')


def get_current_day_int():
    return datetime.datetime.now().strftime('%d')


# ----------- launcher --------- #

do_schedule()
