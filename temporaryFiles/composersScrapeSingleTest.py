#! Web scraper for Composers Site, linked to Firestore

import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from bs4 import BeautifulSoup
import lxml
import requests

def tagToStr(tag):
    if isinstance(tag, str):
        return tag
    else:
        return tagToStr(tag.contents[0])

NONE = 'None'

oppR = requests.get('http://live-composers.pantheonsite.io/opportunity/16235')
oppSoup = BeautifulSoup(oppR.content, 'html.parser')
title = oppSoup.select('.views-field-title .field-content')[0].contents[0] if oppSoup.select('.views-field-title .field-content') else NONE

descriptionTags = oppSoup.select('p') if oppSoup.select('p') else '' #TODO extra spaces are present here 
descriptionList = []
multiContentString = ''
for tag in descriptionTags:
    if len(tag.contents) <= 1:
        descriptionList.append(tagToStr(tag))
    else:
        for element in tag.contents:
            multiContentString += tagToStr(element)
        descriptionList.append(multiContentString)
descriptionList.pop()
description = '\n\n'.join(descriptionList) #TODO description yields multiples of some tags
print(description)




# for tag in descriptionTags: #the tags are fine, in the process of parsing them, you get duplicates
#             print(tag)
#             print('\n\n')
#             if len(tag.contents) <= 1:
#                 descriptionList.append(tagToStr(tag))
#                 #print(f'appended tagToString -----> {tagToStr(tag)}')
#             else: #TODO issue is here because whenever you have <br> or <a> or any nested tag in the <p> tag, you end up duplicating content
#                 for element in tag.contents:
#                     multiContentString += tagToStr(element)
#                 descriptionList.append(multiContentString)
#                 #print(f'appended multiContentString -----> {multiContentString}')