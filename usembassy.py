
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlencode
import pandas as pd




def pull(page=1):
    """
    Searched the website https://www.usembassy.gov/ for '' (which
    returns every post and embassy in a paginated format). This function
    grabs the results from one page. It grabs country, post, and Google
    Maps Embed Url. NOTE: the site returns country. Meaning if a country
    has multiple Posts it will return all posts in that country which
    does _not_ country to the 3 per-page limit.
    """
    # Prepare data
    form_data = {
            'action': 'wpas_ajax_load',
            # Page number parameter
            'page': page,
            'form_data': urlencode({
                # Search query is '' : meaning return all
                'search_query': '',
                'paged': 1,
                'wpas_id': 'iipajaxform',
                'wpas_submit': 1,
            }),
    }

    # Make the request
    r = requests.post(
        'https://www.usembassy.gov/all/wp-admin/admin-ajax.php',
        data=form_data,
    )

    # Parse results
    soup = BeautifulSoup(r.json()['results'], 'html.parser')

    df = [{
        'State': ([ y.get_text() for y in x.find_all('h2')] or [None])[0],
        'Post_Full_Name': ([ y.get_text() for y in z.find_all('strong')] or [None])[0],
        'Google_Map_Url': ([ y['src'] for y in z.find_all('iframe')] or [None])[0],
    }
        ## For all countries
        for x in soup.find_all('div', attrs={'class': 'repe'})
            ## For all posts
            for z in x.find_all('div', attrs={'class': 'cityname'})
    ]
    ## The site returns another format when a country has 1 post and no Google Map.
    ## This logic handles that case.
    df.extend([{
        'State': ([ y.get_text() for y in x.find_all('h2')] or [None])[0],
        'Post_Full_Name': ([ y.get_text() for y in x.find_all('strong')] or [None])[0],
        'Google_Map_Url': ([ y['src'] for y in x.find_all('iframe')] or [None])[0],
    }
        for x in soup.find_all('div', attrs={'class': 'repe'})
    ])

    df = pd.DataFrame(df).drop_duplicates()

    return \
        r.json()['current_page'], \
        r.json()['max_page'], \
        df

def do_pull(page=1):
    """
    Helper function.
    """
    _, _, df = pull(page)
    return df
    

## Pull once to get the number of pages (or calls) needed.
current_page, max_page, df = pull()


## Pull all pages and create an table of the data.
df = pd.concat([
    do_pull(i)
    for i in range(1, max_page + 1)
])

## Write 
print(df)
df.to_csv('usembassy.csv')
