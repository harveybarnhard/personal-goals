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

# Get date of first lesson
date_unix = response['lessons_today'][0]['time']
date_time = datetime.fromtimestamp(date_unix)
date_string = date_time.strftime('%m-%d-%Y')

df = pd.read_csv('https://raw.githubusercontent.com/harveybarnhard/personal-goals/main/data/language.csv')

print(df)
