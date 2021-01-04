import json
import os
import pandas as pd
from datetime import datetime
import duolingo

# Sign in and get daily xp progresss
lingo = duolingo.Duolingo('HarveyBarn', os.getenv('DUOLINGO'))
response = lingo.get_daily_xp_progress()
print(response)
# Get number of xp today
xp = response['xp_today']

# Get date of first lesson today
date_unix = response['lessons_today'][0]['time']
date_time = datetime.fromtimestamp(date_unix).date()
date_string = date_time.strftime('%m-%d-%Y')
df = pd.read_csv('https://raw.githubusercontent.com/harveybarnhard/personal-goals/main/data/raw/language.csv')

# Add a row
df['timestamp'] = df['timestamp'].astype(int)
df['temp'] = df['timestamp'].apply(lambda x: datetime.fromtimestamp(x).date())
max_date = df.temp.max()
if date_time >= max_date:
    if date_time == max_date:
        del df['temp']
        df.loc[df.index.max()] = ['German'] + [date_string] + [xp] + [date_unix]
    else:
        del df['temp']
        df.loc[df.index.max() + 1] = ['German'] + [date_string] + [xp] + [date_unix]
df.to_csv('./data/raw/language.csv', index=False)

# Calculate first monday of week
df['date'] = pd.to_datetime(df['date'])
df['monday'] = df['date'] -  pd.to_timedelta(arg=df['date'].dt.weekday, unit='D')

# collapse by week and language
df = df.groupby(['monday'], as_index=False).agg({
    'xp':'sum'
})
df.rename(columns={'xp':'duolingo_xp'}, inplace=True)
df.to_csv('./data/language.csv', index=False)
