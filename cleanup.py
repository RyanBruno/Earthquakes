
# Imports
import pandas as pd
import re

# Inputs
df = pd.read_csv('usembassy.csv')
df_reference = pd.read_csv('cleanup_reference.csv')
df_cities = pd.read_csv('cities.csv')

## Extract longitude and latitude from the Google Map Embed Url
df = df.dropna(subset = ['Post_Full_Name'])
df['Latitude'] = df['Google_Map_Url'].str.extract(r'!3d(-*\d+\.\d+)')
df['Longitude'] = df['Google_Map_Url'].str.extract(r'!2d(-*\d+\.\d+)')

## Translate N -> + and S -> - ... in our Wikipedia dataset
df_cities['Latitude'] = df_cities['Latitude'].str.replace('N', '')
df_cities['Latitude'] = df_cities['Latitude'].str.replace('S', '-')
df_cities['Longitude'] = df_cities['Longitude'].str.replace('E', '')
df_cities['Longitude'] = df_cities['Longitude'].str.replace('W', '-')


"""
Incorporate the reference dataset. This is a small dataset manually
collected. It's data should overwrite any other data.
"""
df = df.merge(
    df_reference,
    on = 'Post_Full_Name',
    how = 'left',
    suffixes=('', '_Ref'),
)
df = df[df['Drop'] != True]

"""
Create a City column from the Post's full name by removing any prefixes.
"""
df['City'] = df['Post_Full_Name']
df['City'] = df['City'].str.replace('U.S. Consulate in ', '', regex = False)
df['City'] = df['City'].str.replace('U.S. Consulate General in ', '', regex = False)
df['City'] = df['City'].str.replace('U.S. Embassy in ', '', regex = False)
df['City'] = df['City'].str.replace('U.S. Embassy to the', '', regex = False)
df['City'] = df['City'].str.replace('U.S. Embassy ', '', regex = False)
df['City'] = df['City'].str.replace('American Institute in ', '', regex = False)
df['City'] = df['City'].str.replace('U.S. Virtual Embassy to ', '', regex = False)
df['City'] = df['City'].str.replace('U.S. Virtual Presence Post ', '', regex = False)

## Incorporate our open-source city dataset.
df = df.merge(
    df_cities,
    on = 'City',
    how = 'left',
    suffixes=('', '_City'),
)

## This dataset can also work on the country column in the case of
## some city-states.
df = df.merge(
    df_cities,
    left_on = 'City',
    right_on = 'Country',
    how = 'left',
    suffixes=('', '_Country'),
)

## Combine_first if equivalent to coalesce.
## So from top to bottom, left to right take the first non-null value.
df['Latitude'] = df['Latitude_Ref']\
    .combine_first(df['Latitude'])\
    .combine_first(df['Latitude_City'])\
    .combine_first(df['Latitude_Country'])

df['Longitude'] = df['Longitude_Ref']\
    .combine_first(df['Longitude'])\
    .combine_first(df['Longitude_City'])\
    .combine_first(df['Longitude_Country'])


## Subset for readability
df = df[[
    'State',
    'Post_Full_Name',
    'Latitude',
    'Longitude',
]]

## Write the results
print(df)
df.to_csv('cleanup.csv')
