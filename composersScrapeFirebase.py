#! Web scraper for Composers Site, linked to Firebase

import pyrebase

config = {
    "databaseURL": "https://creative-baggage-default-rtdb.firebaseio.com/",
    "apiKey": "AIzaSyAjTneec3uT-hCCsau-afdcQ5lj0y7mnsM",
    "authDomain": "creative-baggage.firebaseapp.com",
    "projectId": "creative-baggage",
    "storageBucket": "creative-baggage.appspot.com",
    "messagingSenderId": "155016155266",
    "appId": "1:155016155266:web:f905d9851dd0c06050249b",
    "measurementId": "G-VBXPC0VFC4"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()

#NoSQL, no rows and columns, 
data = {"Age": 21, "Name": "Kerhonkson Smith", "Owns a Sunny": False}

#database.push(data)
#database.child("Users").child("FirstPerson").set(data)

# honk = database.child("Users").child("FirstPerson").get(data)
# print(honk.val())


#database.child("Users").child("FirstPerson").update({"Name":"Kerhonkson Crawford"})

#database.child("Users").child("FirstPerson").child("Age").remove()

database.child("-NLroILkvf-d6d-Om770").remove()