#------------------------------------#
# import libraries
#------------------------------------#
import csv
import pandas as pd
from geopy.geocoders import Nominatim
from opencage.geocoder import OpenCageGeocode


#------------------------------------#
geolocator = OpenCageGeocode(key="") # YOUR API KEY
#------------------------------------#


#------------------------------------#
# Reads the scraped data from the output of the scraping script
#------------------------------------#
with open("DPD_depots.txt") as f:
    content = f.readlines()
line = [x.strip() for x in content] 
#------------------------------------#

#------------------------------------#
# Formats and cleans the data
#------------------------------------#
address=[];postcode=[];city=[];name=[];depots=[]
line_full=str()
for i in range(len(line)):
    if line[i]!=line[5]:
        line_full=line_full+line[i]+' '
    else:
        if line_full!=line[5] and line[i-1]!=line[5]:
            if (str(line[i-5])!=''): # if the data for a depot has five lines
                name.append(str(line[i-5])) # this is the name of the depots
                address.append(str(line[i-4])+' '+str(line[i-3])) # the address
                city.append(str(line[i-2])) # the city
                postcode.append(str(line[i-1])) # and the postcode
            elif str(line[i-4])!='': # if the data for a depot has four lines
                name.append(str(line[i-4])) # this is the name of the depots
                address.append(str(line[i-3])) # the address
                city.append(str(line[i-2])) # the city
                postcode.append(str(line[i-1])) # and the postcode
            else: # other format
                print('Problem with the address format',line_full)
        line_full=str()    

# Formats the data into a data frame, remove duplicates, sort by postcode alphabetic order
for i in range(len(name)):
         depots.append([name[i],address[i].replace(",",""),city[i],postcode[i]])
depots = pd.DataFrame(depots,columns=['Name','Address','City','Postcode'])
depots=depots.drop_duplicates()
#------------------------------------#


#------------------------------------#
# Geocodes the depots
#------------------------------------#
DPD_depot=[]
for index in range(len(depots)):
    loc=depots.iloc[index]['Address']+' '+depots.iloc[index]['Postcode']
    location = geolocator.geocode(loc) # calls the geocoder
    if location : # if the geocoder succeeded
            lat=location[0]['geometry']['lat']
            lng=location[0]['geometry']['lng']
            if (location[0]['components']['country']!='United Kingdom'): # checks that the obtained location is in the UK
                print("country issue",loc)
            elif (location[0]['confidence']<8): # returns a warning if the confidence level of the geocoder is low. The latitude and longitude are not returned and set to the default value 42
                print(depots.iloc[index]['Postcode'],":",location[0]['confidence'])
                DPD_depot.append([depots.iloc[index]['Name'],depots.iloc[index]['Address'].replace(",",""),depots.iloc[index]['Postcode'],42,42])
            else: # everything went fine!
                DPD_depot.append([depots.iloc[index]['Name'],depots.iloc[index]['Address'].replace(",",""),depots.iloc[index]['Postcode'],lat,lng])
    else:   # if the geocoder failed
                print(depots.iloc[index]['Postcode'],":","location not found")
                DPD_depot.append([depots.iloc[index]['Name'],depots.iloc[index]['Address'].replace(",",""),depots.iloc[index]['Postcode'],42,42])                

# Formats the data into a data frame and outputs it into a csv
DPD_depots = pd.DataFrame(DPD_depot,columns=["Name", "Address", "Postcode","Latitude","Longitude"])
DPD_depots.to_csv("DPD_depots.csv")
#------------------------------------#
