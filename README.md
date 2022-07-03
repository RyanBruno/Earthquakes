## U.S. Department of State – Data Scientist Position – Written Assessment

Below is a list of scripts including their inputs, outputs, and dependencies.



##### usembassy.py

Description: Scrapes https://www.usembassy.gov and collects a list of
	     every U.S. Embassy and Consulate's Country, Full Name,
	     and Google Map embed link.

Outputs:
 - usembassy.csv

Dependencies (pip packages):
 - pandas
 - urllib
 - beautifulsoup4


##### cleanup.py

Description: Creates a cleaned U.S. Embassy and Consulate dateset
	     including the best approximation of their physical
	     buidling's longitude and latitude. It uses two additional
 	     datasets: the cities dataset from wikipedia and a manual
	     cleanup_references.csv dataset manually collected.

Inputs:
 - usembassy.csv
 - cleanup_references.csv
 - cities.csv

Outputs:
 - cleanup.py

Dependencies (pip packages):
 - pandas


##### analysis.py

Description: Collects a tables from
	     (https://en.wikipedia.org/wiki/List_of_cities_by_elevation)
	     listing major cities and their longitude and latitude.

Outputs:
 - cities.py

Dependencies (pip packages):
 - pandas
 - wikipedia


##### analysis.py

Description: Performs the necessary transformations to combine our
	     resulting Embassy and Consulate dataset with the Earthquake
	     dataset to calculate a risk factor as described in the
	     written submission.

Inputs:
 - cleanup.csv
 - Data Set - Earthquakes.xlsx'

Outputs:
 - analysis.csv

Dependencies (pip packages):
 - pandas
 - geopy

