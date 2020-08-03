# Shows the top artists for a user
import json
import pprint
import sys
from datetime import datetime
from datetime import timedelta


# import export as export
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

def date_from_days(mean):
    cyear = int(mean.days / 365)
    cmonth = int(((mean.days / 365) - cyear) * 12)
    cday = 1
    if cmonth in (1, 3, 5, 7, 8, 10, 12):
        cday = int(((((mean.days / 365) - cyear) * 12) - cmonth) * 31)
    elif cmonth in (4, 6, 9, 11):
        cday = int(((((mean.days / 365) - cyear) * 12) - cmonth) * 30)
    elif cmonth == 2:
        cday = int(((((mean.days / 365) - cyear) * 12) - cmonth) * 28)
    new_dt = datetime(year=cyear, month=cmonth, day=cday)
    return new_dt

def date_from_days_list(mean):
    cyear = int(mean.days / 365)
    cmonth = int(((mean.days / 365) - cyear) * 12)
    cday = 1
    if cmonth in (1, 3, 5, 7, 8, 10, 12):
        cday = int(((((mean.days / 365) - cyear) * 12) - cmonth) * 31)
    elif cmonth in (4, 6, 9, 11):
        cday = int(((((mean.days / 365) - cyear) * 12) - cmonth) * 30)
    elif cmonth == 2:
        cday = int(((((mean.days / 365) - cyear) * 12) - cmonth) * 28)
    datelist = [cyear, cmonth, cday]
    return datelist

# def is_leap_year(year):
#     dyear = year/4
#     if int(dyear) == dyear:
#         return True
#     else:
#         return False



if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit(),

scope = 'user-library-read'

token = util.prompt_for_user_token(username, scope, client_id='***************',
                                                          client_secret='***************', redirect_uri='https://accounts.spotify.com/en/status')



if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace= False

    results = sp.current_user_saved_tracks(limit = 50)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    release_delta = timedelta(seconds=0)
    mean = timedelta(seconds=0)
    j = 99
    times = 0
    total = 0

    for i in range(0,len(tracks),100):
        dates = []
        for item in tracks[i:j]:
            release_date = item['track']['album']['release_date']
            if (item['track']['album']['release_date_precision'] == 'day'):
                release_dt = datetime.strptime(release_date, '%Y-%m-%d')
                if release_dt.month in (1,3,5,7,8,10,12):
                    release_delta = timedelta(days=(release_dt.year * 365) + (release_dt.month*31) + (release_dt.day))
                elif release_dt.month in (4, 6, 9, 11):
                    release_delta = timedelta(days=(release_dt.year * 365) + (release_dt.month * 30) + (release_dt.day))
                elif release_dt.month == 2:
                    release_delta = timedelta(days=(release_dt.year * 365) + (release_dt.month*28) + (release_dt.day))
                dates.append(release_delta)
            if (item['track']['album']['release_date_precision'] == 'month'):
                release_dt = datetime.strptime(release_date, '%Y-%m')
                if release_dt.month in (1,3,5,7,8,10,12):
                    release_delta = timedelta(days=(release_dt.year * 365) + (release_dt.month*31))
                elif release_dt.month in (4, 6, 9, 11):
                    release_delta = timedelta(days=(release_dt.year * 365) + (release_dt.month * 30))
                elif release_dt.month == 2:
                    release_delta = timedelta(days=(release_dt.year * 365) + (release_dt.month*28))
                dates.append(release_delta)
            if (item['track']['album']['release_date_precision'] == 'year'):
                release_dt = datetime.strptime(release_date, '%Y')
                release_delta = timedelta(days=(release_dt.year*365))
                dates.append(release_delta)
        sum = dates[0]
        # print(sum)
        for date in dates[1:]:
            sum += date
        avg = (sum / len(dates))
        mean+=avg
        j +=100
        total += len(dates)
        times += 1
    mean = mean/times
    new_dt = date_from_days(mean)
    time_now = datetime.now()
    diff = time_now - new_dt
    age = date_from_days_list(diff)
    # print(new_dt)
    # print()
    print(sp.current_user()['display_name'])
    print()
    if (age[0] < 10):
        print("Your Spotify Age is {0} years, {1} months, and {2} days. Your taste in music is pretty new!".format(age[0], age[1], age[2]))
    elif (age[0] < 20):
        print("Your Spotify Age is {0} years, {1} months, and {2} days. You've been around a little bit longer.".format(age[0], age[1], age[2]))
    elif (age[0] < 30):
        print("Your Spotify Age is {0} years, {1} months, and {2} days. You probably have 3 kids and a mortgage by now.".format(age[0], age[1], age[2]))
    else:
        print("Your Spotify Age is {0} years, {1} months, and {2} days. You're an old timer!".format(age[0], age[1], age[2]))
else:
    print("Can't get token for", username)

