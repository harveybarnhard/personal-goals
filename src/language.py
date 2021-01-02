import duolingo
import json
import os

# Sign in and get daily xp progresss
lingo = duolingo.Duolingo('HarveyBarn', os.getenv('DUOLINGO'))
response = lingo.get_daily_xp_progress()
# Get number of xp today
xp = response['xp_today']
# Get date of first lesson
date = response['lessons_today'][0]['time']
#lingo.get_language_progress('de')
