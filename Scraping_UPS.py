#------------------------------------#
# import libraries
#------------------------------------#
import urllib.request
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
#------------------------------------#



#------------------------------------#
# Initiate the browser: Firefox
#------------------------------------#
url='https://www.ups.com/dropoff/'
driver = webdriver.Firefox()
#------------------------------------#


#------------------------------------#
# Read the list of postcodes - 
# Warning: this is a long list!
#------------------------------------#
data = pd.read_csv("Postcodes_master.csv")
postcodes=data["Postcode"]
#------------------------------------#

# Output file
f = open("UPS_depots.txt", "w") 

#------------------------------------#
# Core of the code, loop over postcodes
#------------------------------------#

for index in range(len(postcodes)):
    pstcd=postcodes[index]
    time.sleep(2)
    print(pstcd) # prints the currently used postcode
    driver.get(url) # browser opens the UPS page
    time.sleep(2)
            
    # selects UK in the list of countries    
    el = driver.find_element_by_name("country")
    for option in el.find_elements_by_tag_name('option'):
        if option.text == 'United Kingdom':
            option.click()
            break

    # selects UPS customer center in the field "Location Type"
    driver.find_element_by_id("a_show_all_options").click()
    time.sleep(1)
    driver.find_element_by_id("a_sub_filter_loc_type").click()
    time.sleep(1)
    driver.find_element_by_id("loc_type_001").click()
    time.sleep(1)    
   
    # enters the postcode and initiate the search
    postcode_query = driver.find_element_by_name("txtquery")
    postcode_query.clear()
    postcode_query.send_keys(pstcd)
    postcode_query.send_keys(Keys.ENTER)
    time.sleep(3)

    # reads the results: name, address, etc of the nearest center and prints them to the output file
    results=driver.find_elements_by_css_selector('.seccol5.marginEnd.group.clearfix')
    list_cc=[]
    for result in results:
        list_cc.append(result.text)
    for line in list_cc:
        f.write(line)
#------------------------------------#


driver.quit() #closes the browser 
f.close() # and the output file
