
## Imports
import pandas as pd
import wikipedia as wp

## Utilize the wikipedia package to grabe the html of this page.
html_e = wp.page('List_of_cities_by_elevation').html().encode('UTF-8')


"""
Pandas can be used to read HTML tables. In this case it works great.
[1] needs to be used because the first tables is the table of contents.
"""
df = pd.concat([
    pd.read_html(html_e)[1],
])

## This script errors if the input columns change.
assert list(df) == ['Country/Territory', 'City Name/s', 'Continental Region', 'Latitude', 'Longitude', 'Population', 'Elevation (m)'],\
        "Input columns have changed"
df.columns = [
    'Country', 'City','Region', 'Latitude', 'Longitude',
    '_', '__',
]
df = df[['Country', 'City','Latitude', 'Longitude']]

df = df.groupby([
        'City',
        'Country',
]).agg({
    'Latitude': 'first',
    'Longitude': 'first',
})


## Write the results
print(df)
df.to_csv('cities.csv')
