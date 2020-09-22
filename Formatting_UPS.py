#------------------------------------#
# import libraries
#------------------------------------#
import csv
import requests
import postcodes_io_api
import pandas as pd    
from geopy.geocoders import Nominatim
from opencage.geocoder import OpenCageGeocode
#------------------------------------#

#------------------------------------#
geolocator = OpenCageGeocode(key="") # YOUR API KEY
#------------------------------------#


#------------------------------------#
# Reads the scraped data from the output of the scraping script
#------------------------------------#
with open("UPS_depots.txt") as f:
    content = f.readlines()
line = [x.strip() for x in content] 
#------------------------------------#

#------------------------------------#
# Formats and cleans the data
#------------------------------------#
address=[];postcode=[];name=[];depot=[]
word="el: "
for i in range(len(line)):
    if (line[i].find(word)>0): # identify where the string el: is located: this corresponds to the line with the phone number and we are interesting in the two lines before this one as they contain the name and address of the customer center
        nm=line[i-2].replace(" (LOCATOR)","")       
        name.append(nm) # name of the depot
        ddrss=line[i-1].split(",") # address of the depot
        pstcd=ddrss[-1].strip() # postcode of the depot
        postcode.append(pstcd)
        ddrss=' '.join(ddrss[:len(ddrss)-2])
        address.append(ddrss)
        dpt=[nm,ddrss,pstcd] # full name + address + postcode of the depot
        depot.append(dpt)

# Formats the data into a data frame, remove duplicates, sort by postcode alphabetic order
depots = pd.DataFrame(depot,columns=["Name", "Address", "Postcode"])
depots=depots.drop_duplicates()
depots=depots.sort_values("Postcode")
depots=depots.reset_index(drop=True)
#------------------------------------#

#------------------------------------#
# Geocodes the depots
#------------------------------------#
UPS_depot=[]
for index in range(len(depots)):
    loc=depots.iloc[index]['Address']+depots.iloc[index]['Postcode']
    print(loc)
    location = geolocator.geocode(loc) # calls the geocoder
    if location : # if the geocoder succeeded
            lat=location[0]['geometry']['lat']
            lng=location[0]['geometry']['lng']
            if (location[0]['components']['country']!='United Kingdom'): # checks that the obtained location is in the UK
                print("country issue",loc)
            elif (location[0]['confidence']<8): # returns a warning if the confidence level of the geocoder is low. The latitude and longitude are not returned and set to the default value 42
                print(depots.iloc[index]['Postcode'],":",location[0]['confidence'])
                UPS_depot.append([depots.iloc[index]['Name'],depots.iloc[index]['Address'].replace(",",""),depots.iloc[index]['Postcode'],42,42])
            else: # everything went fine!
                UPS_depot.append([depots.iloc[index]['Name'],depots.iloc[index]['Address'].replace(",",""),depots.iloc[index]['Postcode'],lat,lng])
    else:   # if the geocoder failed
                print(depots.iloc[index]['Postcode'],":","location not found")
                UPS_depot.append([depots.iloc[index]['Name'],depots.iloc[index]['Address'].replace(",",""),depots.iloc[index]['Postcode'],42,42])                

# Formats the data into a data frame and outputs it into a csv
UPS_depots = pd.DataFrame(UPS_depot,columns=["Name", "Address", "Postcode","Latitude","Longitude"])
UPS_depots.to_csv("UPS_depots.csv")
#------------------------------------#
