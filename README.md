# About
Web scraping of the JavaScript-based [UK UPS website](https://www.ups.com/dropoff/) and [UK DPD website](https://www.dpd.co.uk/apps/depotfinder/index.jsp)


## Content
* Postcode_master.csv: list of ~7.000 UK postcodes (see [this page](https://github.com/ganetin/UK_postcodes) to generate the list)
* Scraping_UPS.py and Scraping_DPD.py: using web scraping find the UPS Customer Center/DPD depots in the UK closest to the postcodes in Post.csv. Return a txt file UPS_depots.txt/DPD_depots.txt
* Formatting_UPS.py and Formatting_DPD.py: Formats the data scraped for the UPS/DPD depots into a more easily manipulable format and geocode the addresses of the depots. Returns UPS_depots.csv/DPD_depots.csv
* UPS_depots.csv/DPD_depots.csv: files containing for each DPD/UPS depot their address, postcode and coordinates (Latitude,Longitude)

## Prerequisites:
Web-scraping: 
* [selenium](https://selenium-python.readthedocs.io/)
* [geckodriver](https://pypi.org/project/geckodriver-autoinstaller/)
* [Python csv module](https://docs.python.org/3/library/csv.html)
* Python [time](https://docs.python.org/3/library/time.html) module

Formatting:
* [pandas](https://pandas.pydata.org/)
* [geopy](https://geopy.readthedocs.io/en/stable/) and if need be an API key for your favorite geocoder (here [OpenCageGeocode](https://opencagedata.com/))
* [Python csv module](https://docs.python.org/3/library/csv.html)


## Improvements needed:
Scraping_*py:
* adjust the waiting time to speed up the process
* better handling of errors
* inclde the formatting of the data in the same code instead of having another python script Formatting_*py

## License
MIT License

## Author
Dr. Morgane FORTIN, Sept. 2020
