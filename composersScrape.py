#! Web scraper for Composers Site, saves data in CSV file formatted for upload to Wix

#TODO put some sections inside functions

import os
import csv
import string
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from locationSets import countriesSet, citiesSet, countryToCity, statesSet
import tagLists
from tagLists import typeOfOpportunity, keywords, partTime, fullTime

OPP_LINK = 'http://live-composers.pantheonsite.io'
PAGE_LINK = 'http://live-composers.pantheonsite.io/opps/results/taxonomy%3A13?page=' #pages start from 0
NONE = 'None'
title = ''
deadline = ''
location = ''
description = ''
website = ''
APPROVED = 'FALSE'

os.chdir('D:\Google Drive\Creative Baggage\webScraping')

dataStorage = [] #list of dicts

def tagToStr(tag): #recursive function that converts tag and its contents to string, including all nested tags
    if isinstance(tag, str):
        return tag
    else:
        if tag.contents:
            return tagToStr(tag.contents[0])
        else:
            return ''

r = requests.get('http://live-composers.pantheonsite.io/opps/results/taxonomy%3A13')
soup = BeautifulSoup(r.content, 'html.parser')
opportunityRows = soup.select('.views-row .field-content a')
oppLinks = [row['href'] for row in opportunityRows]
maxPage = soup.select('.pager-last a')[0].attrs['href'][-1]

csvfile = open('composersSite.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csvfile, delimiter=',')
writer.writerow(['title', 'dueDate', 'location', 'notes', 'link', 'typeOfOpportunity', 'approved', 'keywords']) #8 columns

for i in range(int(maxPage) + 1):

    pageR = requests.get(PAGE_LINK + str(i))
    soup = BeautifulSoup(pageR.content, 'html.parser')
    opportunityRows = soup.select('.views-row .field-content a')
    oppLinks = [row['href'] for row in opportunityRows]

    for oppLink in oppLinks:
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
        if not deadline == NONE:
            deadline += ' 23:59'
            deadline = datetime.strptime(deadline, '%d %b %Y %H:%M')
            deadline = datetime.strftime(deadline, '%d/%m/%Y %H:%M')
        print(deadline)

        website = oppSoup.select('.views-field-field-opp-url-url a')[0].contents[0] if oppSoup.select('.views-field-field-opp-url-url a') else ''
        
        #LOCATION -------------------------------------------------------------------------------------------
        location = ''
        state = None
        city = None
        country = None
        found = False
        
        i = 0
        while not found and i < len(citiesSet):
            result = description.find(citiesSet[i])
            if result >= 0:
                found = True
                city = citiesSet[i]
                country = countryToCity[i]
            i += 1
        
        if country == 'United States':
            found = False
            i = 0        
            while not found and i < len(statesSet):
                result = description.find(statesSet[i])
                if result >= 0:
                    found = True
                    state = statesSet[i]
                i += 1
        if not city == None:
            location += city
        if not state == None:
            location += ', ' + state
        if not country == None:
            location += ', ' + country
        if len(location) == 0:
            location = 'Online'

        #Tags -------------------------------------------------------------------------------------------
        #Wix tag formatting - ["tag1","tag2"]
        tagsSet = set()
        descriptionLower = description.lower()
        for keyword in keywords:
            if descriptionLower.find(keyword) >= 0:
                tagsSet.add(keyword)
        for tag in tagsSet:
            keywordsString += f'"{tag}",'

        if keywordsString == '[':
            keywordsString = ''
        else:
            keywordsString = keywordsString[:-1] + ']'
        
        for type in typeOfOpportunity:
            if descriptionLower.find(type) >= 0:
                if type in partTime:
                    typeOfOppString += f'"{tagLists.PART_TIME_JOB}",'
                elif type in fullTime:
                    typeOfOppString += f'"{tagLists.FULL_TIME_JOB}",'
                else:
                    typeOfOppString += f'"{string.capwords(type)}",'
        if typeOfOppString == '[':
            typeOfOppString = '["Other"]'
        else:
            typeOfOppString = typeOfOppString[:-1] + ']'

        currentRow = [title, deadline, location, description, website, typeOfOppString, APPROVED, keywordsString]
        writer.writerow(currentRow)
            
csvfile.close()


#world cities list attribution - https://simplemaps.com/data/world-cities