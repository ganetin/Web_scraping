#------------------------------------#
# import libraries
#------------------------------------#
import urllib.request
from selenium import webdriver
import time
import pandas as pd


#------------------------------------#
# Initiate the browser: Firefox
#------------------------------------#
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
f = open("DPD_depots.txt", "w") 

#------------------------------------#
# Core of the code, loop over postcodes
#------------------------------------#
for index in range(len(postcodes)):
    code=postcodes[index]
    print(code) # prints the currently used postcode
    url='https://www.dpd.co.uk/apps/depotfinder/index.jsp#depot/postcode/'+code.replace(' ','%20')
    driver.get(url)  # browser opens the DPD page for the given postcode
    time.sleep(3)

    # reads the results: name, address, etc of the nearest center and prints them to the output file
    results = driver.find_elements_by_xpath("//*[@id='page_content']//*[@class='module']//*[@class='module-body']//*[@class='form-body']//*[@class='row clearfix']//*[@class='column small-12 mini-5 medium-5 large-5 tight-left']")
    result=results[0].text
    f.write(result+'\n\n')
    f.write('\n')    
    time.sleep(5)

driver.quit() #closes the browser 
f.close() # and the output file



