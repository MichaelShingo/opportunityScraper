# Web scraper for Composers Site, saves data in CSV file formatted for upload to Wix
#World cities list attribution - https://simplemaps.com/data/world-cities
#TODO put some sections inside functions

import csv
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from helperFunctions import tagToStr, findLocation, findOppTypeTags, findKeywordTags

OPP_LINK = 'http://live-composers.pantheonsite.io'
PAGE_LINK = 'http://live-composers.pantheonsite.io/opps/results/taxonomy%3A13?page=' #pages start from 0
NONE = 'None'
APPROVED = 'FALSE'

title = ''
deadline = '' #if none provided, use NONE
location = '' #if none found, use ONLINE
description = ''
website = ''

#SCRAPING ---------------------------------------------------------
r = requests.get('http://live-composers.pantheonsite.io/opps/results/taxonomy%3A13')
soup = BeautifulSoup(r.content, 'html.parser')
opportunityRows = soup.select('.views-row .field-content a')
oppLinks = [row['href'] for row in opportunityRows]
maxPage = soup.select('.pager-last a')[0].attrs['href'][-1]

#csv file created, use this format for data to match Wix collection
csvfile = open('composersSite.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csvfile, delimiter=',')
writer.writerow(['title', 'dueDate', 'location', 'notes', 'link', 'typeOfOpportunity', 'approved', 'keywords'])

for i in range(int(maxPage) + 1): #loops through all pages
    pageR = requests.get(PAGE_LINK + str(i))
    soup = BeautifulSoup(pageR.content, 'html.parser')
    opportunityRows = soup.select('.views-row .field-content a')
    oppLinks = [row['href'] for row in opportunityRows]

    for oppLink in oppLinks: #loops through all opportunities on each page
        keywordsString = '['
        typeOfOppString = '['
        oppR = requests.get(OPP_LINK + oppLink)
        oppSoup = BeautifulSoup(oppR.content, 'html.parser')
        title = oppSoup.select('.views-field-title .field-content')[0].contents[0] if oppSoup.select('.views-field-title .field-content') else NONE
        descriptionTags = oppSoup.select('p') if oppSoup.select('p') else '' #TODO extra spaces are present here 
        descriptionList = []
        for tag in descriptionTags:
            for element in tag.contents: 
                descriptionList.append(tagToStr(element))
        descriptionList.pop()
        description = '\n\n'.join(descriptionList)
        deadline = oppSoup.select('.date-display-single')[0].contents[0] if oppSoup.select('.date-display-single') else NONE
        if not deadline == NONE: #deadline is 23:59 on the date provided, new date regex needed depending on site's date format
            deadline += ' 23:59'
            deadline = datetime.strptime(deadline, '%d %b %Y %H:%M')
            deadline = datetime.strftime(deadline, '%d/%m/%Y %H:%M')

        website = oppSoup.select('.views-field-field-opp-url-url a')[0].contents[0] if oppSoup.select('.views-field-field-opp-url-url a') else ''
        
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