import pandas as pd
import datetime

# Load data
df = pd.read_csv('https://raw.githubusercontent.com/harveybarnhard/endur/main/data/strava_activities_sub.csv')

# create year column
df['date'] = pd.to_datetime(df['monday'])
df['year'] = df['monday'].str[-4:]

# Create weekly total moving time column
df['total_moving_time'] = df.loc[:,df.columns.str.contains('moving_time')].sum(axis=1)

# Create weekly total cycling distance
df['total_cycling_time'] = df.loc[:,df.columns.str.contains('Ride_moving_time')].sum(axis=1)

# Subset to relevant columns
df = df[['year', 'date', 'monday', 'total_moving_time', 'total_cycling_time', 'Run_distance', 'Ride_total_elevation_gain', 'Run_total_elevation_gain']]
# Create cumulative dataset
df2 = df.groupby(['year', 'date']).sum() \
        .groupby(level=0).cumsum().reset_index()
new_names = [(i,i+'_cum') for i in df2.iloc[:, 2:].columns.values]
df2.rename(columns = dict(new_names), inplace=True)
del df2['year']

# Merge weekly and cumulative columns
df = df.merge(df2, on='date', how='outer')
del df['date']

# Write data
df.to_csv('./data/fitness.csv', index=False)
