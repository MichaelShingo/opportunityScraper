# Web scraper for hyperallergic.com, saves data in CSV file formatted for upload to Wix
#World cities list attribution - https://simplemaps.com/data/world-cities

import csv
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from helperFunctions import tagToStr, findLocation, findOppTypeTags, findKeywordTags

NONE = 'None'
APPROVED = 'FALSE'

#SCRAPING ---------------------------------------------------------
r = requests.get('https://hyperallergic.com/818473/opportunities-may-2023/')
soup = BeautifulSoup(r.content, 'html.parser')
oppContainer = soup.select('#pico > p')

# csv file created, use this format for data to match Wix collection
csvfile = open('hyperallergicScrape.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csvfile, delimiter=',')
writer.writerow(['title', 'dueDate', 'location', 'notes', 'link', 'typeOfOpportunity', 'approved', 'keywords'])

for i in range(2, len(oppContainer)):
    title = ''
    deadline = '' #if none provided, use NONE
    location = '' #if none found, use ONLINE
    description = ''
    website = ''

    titleList = oppContainer[i].findChildren('b')
    if len(titleList) == 2:
        title = titleList[1].text
    elif len(titleList) == 1:
        title = titleList[0].text
    else:
        title = ''

    try:
        website = oppContainer[i].findChild('a').attrs['href']
    except:
        website = ''

    contentList = oppContainer[i].contents
    for i in range(len(contentList)):
        if str(contentList[i]) == '<br/>':
            deadline = contentList[i + 1][10:-2]
            description = contentList[i - 1]

    if '(' in deadline:
        indexPar = deadline.index('(')
        deadline = deadline[0:indexPar - 1]

    #DEADLINE -------------------------------------------------------------------------------------------
    if deadline != '': #deadline is 23:59 on the date provided, new date regex needed depending on site's date format
        deadline += ' 23:59'
        deadline = datetime.strptime(deadline, '%B %d, %Y %H:%M')
        deadline = datetime.strftime(deadline, '%d/%m/%Y %H:%M')

    #LOCATION -------------------------------------------------------------------------------------------
    location = findLocation(description) 

    # #Tags -------------------------------------------------------------------------------------------
    keywordsString = '['
    typeOfOppString = '['
    descriptionLower = description.lower()
    keywordsString = findKeywordTags(descriptionLower)
    typeOfOppString = findOppTypeTags(descriptionLower)

    #put all data into a list, which becomes the row in the csv file
    currentRow = [title, deadline, location, description, website, typeOfOppString, APPROVED, keywordsString]
    writer.writerow(currentRow)
   
csvfile.close()