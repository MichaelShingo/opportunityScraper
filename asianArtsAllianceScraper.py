#! Web scraper for American Asian Arts Alliance Site, saves data in CSV file formatted for upload to Wix
#World cities list attribution - https://simplemaps.com/data/world-cities

#TODO pull location from location field....

import csv
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from helperFunctions import tagToStr, findLocation, findOppTypeTags, findKeywordTags

OPP_LINK = 'https://www.aaartsalliance.org'
PAGE_LINK = 'https://www.aaartsalliance.org'
NONE = 'None'
APPROVED = 'FALSE'

title = ''
deadline = '' #if none provided, use NONE
location = '' #if none found, use ONLINE
description = ''
website = ''

#SCRAPING ---------------------------------------------------------
r = requests.get('https://www.aaartsalliance.org/opportunities')
soup = BeautifulSoup(r.content, 'html.parser')
opportunityRows = soup.select('.opportunity a')
oppLinks = [row['href'] for row in opportunityRows]

# csv file created, use this format for data to match Wix collection
csvfile = open('asianArtsAlliance.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csvfile, delimiter=',')
writer.writerow(['title', 'dueDate', 'location', 'notes', 'link', 'typeOfOpportunity', 'approved', 'keywords'])

for oppLink in oppLinks: #loops through all opportunities on each page
    keywordsString = '['
    typeOfOppString = '['
    oppR = requests.get(OPP_LINK + oppLink)
    oppSoup = BeautifulSoup(oppR.content, 'html.parser')
    title = oppSoup.select('.large-title')[0].contents[0] if oppSoup.select('.large-title') else NONE
    descriptionList = []

    descriptionTags = oppSoup.select('.order-1')[1] if oppSoup.select('.order-1') else '' #selects description box
    for pageElement in descriptionTags.children: #how to made one additional \n on <br>'s??? 
        innerText = pageElement.get_text()
        innerText = innerText.replace('\t', '')
        innerText = innerText.replace('  ', '')
        innerText = innerText.replace('\n', '\n\n')
        if innerText != '\n':
            descriptionList.append(innerText)
    descriptionList.pop()
    description = ''.join(descriptionList[1:])
    deadlineList = oppSoup.select('.col-8')[1]#.contents[0] if oppSoup.select('.date-display-single') else NONE
    deadlinePre= deadlineList.select('div')[1].contents[0]
    deadline = ''
    deadline = deadlinePre if deadlinePre != 'Rolling' else NONE

    if not deadline == NONE: #deadline is 23:59 on the date provided, new date regex needed depending on site's date format
        deadline += ' 23:59'
        deadline = datetime.strptime(deadline, '%b %d, %Y %H:%M')
        deadline = datetime.strftime(deadline, '%d/%m/%Y %H:%M')

    secondColumn = oppSoup.select('.order-0')[1].select('a')
    website = secondColumn[len(secondColumn) - 1]['href']
    
    #LOCATION -------------------------------------------------------------------------------------------
    #TODO improve the location function, prioritize finding US states? except Georgia
    location = findLocation(description) 
    
    #Tags -------------------------------------------------------------------------------------------
    descriptionLower = description.lower()
    keywordsString = findKeywordTags(descriptionLower)
    typeOfOppString = findOppTypeTags(descriptionLower)
    
    #put all data into a list, which becomes the row in the csv file
    currentRow = [title, deadline, location, description, website, typeOfOppString, APPROVED, keywordsString]
    writer.writerow(currentRow)
            
csvfile.close()