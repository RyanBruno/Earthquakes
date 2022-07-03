
## Imports
import numpy as np
import pandas as pd
import re
from geopy.distance import EARTH_RADIUS


## Imputs
df_posts = pd.read_csv('cleanup.csv')
df_earthquakes = pd.read_excel('Data Set - Earthquakes.xlsx')


## Subset data for clarity
df_posts = df_posts[[
    'Post_Full_Name',
    'Latitude',
    'Longitude',
]]


df_earthquakes = df_earthquakes[[
    # Time
    'Year',
    'Mo',
    'Dy',
    'Hr',
    'Mn',
    'Sec',
    # Location
    'Latitude',
    'Longitude',
    'Mag',
]]
## END: Subset data for clarity

## If Mag is null it causes errors in some computations
df_earthquakes = df_earthquakes.dropna(subset = ['Mag'])

"""
This is equivalent to a SQL join on 1=1.
That means that a row will be created for every Embassy and Consulate
to every earthquake.
"""
df_posts['1'] = '1'
df_earthquakes['1'] = '1'


df = pd.merge(
    df_posts,
    df_earthquakes,
    on = '1',
    suffixes=('', '_Earthquake'),
)

## END: Join 1=1

## Calculates the distance between two coordinate on the globe
def great_circle_distance(src_lats, src_longs, dest_lats, dest_longs):
    # Convert from degrees to radians.
    src_lats = src_lats.apply(np.deg2rad)
    src_longs = src_longs.apply(np.deg2rad)
    dest_lats = dest_lats.apply(np.deg2rad)
    dest_longs = dest_longs.apply(np.deg2rad)

    # grab sines
    src_lat_sin = src_lats.apply(np.sin)
    dest_lat_sin = dest_lats.apply(np.sin)
    # grab cosines
    src_lat_cos = src_lats.apply(np.cos)
    dest_lat_cos = src_lats.apply(np.cos)

    lng_deltas = dest_longs.subtract(src_longs)
    lng_delta_cos = lng_deltas.apply(np.cos)
    lng_delta_sin = lng_deltas.apply(np.sin)

    return EARTH_RADIUS * np.arctan2(
        np.sqrt(
            (dest_lat_cos * lng_delta_sin) ** 2 +
            (src_lat_cos * dest_lat_sin - src_lat_sin * dest_lat_cos * lng_delta_cos) ** 2
        ),
        src_lat_sin * dest_lat_sin + src_lat_cos * dest_lat_cos * lng_delta_cos
    )


## Calculate the distance between each post and earthquake
df['Distance'] = great_circle_distance(
    df['Latitude'],
    df['Longitude'],
    df['Latitude_Earthquake'],
    df['Longitude_Earthquake'],
)



# Normalize distance
df['Distance_Normal'] = (df['Distance'] - np.min(df['Distance'])) / np.max(df['Distance'])
# Invert distance on the normal scale
df['Distance_Normal'] = 1 - df['Distance_Normal']
# Add 1 or next step wont work
df['Distance_Normal'] = df['Distance_Normal'] + 1
# Apply a exponential transformation
df['Distance_Normal'] = df['Distance_Normal'] * df['Distance_Normal']
# Re-normalize
df['Distance_Normal'] = (df['Distance_Normal'] - np.min(df['Distance_Normal'])) / np.max(df['Distance_Normal'])
# Add 1 or next step wont work
df['Distance_Normal'] = df['Distance_Normal'] + 1

## Removes Quakes > 250 km
#df[df['Distance'] > 250]['Distance_Normal'] = 0

# Normalize Magnitude
df['Mag_Normal'] = (df['Mag'] - np.min(df['Mag'])) / np.max(df['Mag'])
# Add 1 or next step wont work
df['Mag_Normal'] = df['Mag_Normal'] + 1


# Finally multiply transformed distance and magnitude
df['Risk'] = df['Distance_Normal'] * df['Mag_Normal']

# Scale Risk to a 0-100 scale
df['Risk'] = ((df['Risk'] - np.min(df['Risk'])) / np.max(df['Risk'])) * 100


# Aggregate an average risk for each post from each earthquake
df = df.groupby(
    'Post_Full_Name',
).agg({
    'Risk': 'mean',
    'Longitude': 'max',
    'Latitude': 'max',
})

# Re-Scale Risk to a 0-100 scale
df['Risk'] = ((df['Risk'] - np.min(df['Risk'])) / (np.max(df['Risk']) - np.min(df['Risk']))) * 100

# Write
df.to_csv('analysis.csv')
print(df)



