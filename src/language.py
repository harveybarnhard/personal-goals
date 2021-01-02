import duolingo
import json
import os
import pandas as pd
from datetime import datetime

# Sign in and get daily xp progresss
lingo = duolingo.Duolingo('HarveyBarn', os.getenv('DUOLINGO'))
response = lingo.get_daily_xp_progress()
# Get number of xp today
xp = response['xp_today']

# Get date of first lesson today
date_unix = response['lessons_today'][0]['time']
date_time = datetime.fromtimestamp(date_unix).date()
date_string = date_time.strftime('%m-%d-%Y')
df = pd.read_csv('https://raw.githubusercontent.com/harveybarnhard/personal-goals/main/data/raw/language.csv')

# Add a row
df['temp'] = datetime.fromtimestamp(df.timestamp).date()
max_date = df.temp.max()
if date_time >= max_date:
    if date_time == max_date:
        del df['temp']
        df.loc[df.index.max()] = ['German'] + [date_string] + [xp] + [date_unix]
    else:
        del df['temp']
        df.loc[df.index.max() + 1] = ['German'] + [date_string] + [xp] + [date_unix]
df.to_csv('./data/raw/language.csv', index=False)
