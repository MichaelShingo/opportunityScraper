from locationSets import countriesSet, citiesSet, countryToCity, statesSet
import tagLists
from tagLists import typeOfOpportunity, keywords, partTime, fullTime
import string

ONLINE = 'Online'

def tagToStr(tag): #recursive function that converts tag and its contents to string, including all nested tags
    if isinstance(tag, str):
        return tag
    else:
        if tag.contents:
            return tagToStr(tag.contents[0])
        else:
            return ''

def findLocation(description):
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
        location = ONLINE

    return location

def findOppTypeTags(descriptionLower):
    #Wix tag formatting - ["tag1","tag2"]
    result = '['
    for type in typeOfOpportunity:
        if descriptionLower.find(type) >= 0:
            if type in partTime:
                result += f'"{tagLists.PART_TIME_JOB}",'
            elif type in fullTime:
                result += f'"{tagLists.FULL_TIME_JOB}",'
            else:
                result += f'"{string.capwords(type)}",'
    if result == '[':
        result = '["Other"]'
    else:
        result = result[:-1] + ']'
    return result

def findKeywordTags(descriptionLower):
    result = '['
    tagsSet = set()
    for keyword in keywords:
        if descriptionLower.find(keyword) >= 0:
            tagsSet.add(keyword)
    for tag in tagsSet:
        result += f'"{tag}",'

    if result == '[':
        result = ''
    else:
        result = result[:-1] + ']'
    return result