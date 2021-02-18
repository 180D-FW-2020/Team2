from firebase import firebase
from datetime import datetime
import json
#pip install git+https://github.com/ozgur/python-firebase

user_id = 'jackielam'
db_name = 'team2-4ffc1/stats/'

firebase = firebase.FirebaseApplication("https://team2-4ffc1-default-rtdb.firebaseio.com/", None)
tasks = ['stretching', 'breathing', 'talking to friends']

class userStats:
    def __init__(self, user_id, firebase, db_name):
        self.user_id = user_id
        self.firebase = firebase
        self.db_name = db_name
        self.initial_data = { 

            'Tasks': {
                tasks[0]: 0,
                tasks[1]: 0,
                tasks[2]: 0
            },
            'Messages': {
                'Sent' : {
                    'person': 'message'
                },

                'Received' : {
                    'person': 'message'
                }
            },
            'Mood' : {

                'Moods' : ['mood1'], #list of moods all lowercase
                'Songs' : {
                    'song by artist' : 'spotify link'
                }
            } 
        }

    def createEntry(self, current_date):
        add = self.firebase.post(self.db_name + self.user_id + '/' + current_date, self.initial_data)
        print("Created Entry: ", add)
        return add

    def retEntryDate(self):
        current_date = datetime.now().strftime("%m-%d-%Y")
        retrieved_stats = self.retrieveStats(current_date)
        #Check if entry exits, if not, create an initial one
        if(retrieved_stats == None):
            self.createEntry(current_date)
            retrieved_stats = self.retrieveStats(current_date)
            
        key = list(retrieved_stats.keys())[0]
        print("Received stats:", retrieved_stats[key])
        return retrieved_stats[key], key, current_date
    
    def addMessage(self, sent_received, person, message):
        data, key, current_date = self.retEntryDate()
        if sent_received == 'Sent':
            if data['Messages']['Sent'].__contains__(person):
                data['Messages']['Sent'][person].append(message)
            else:
                data['Messages']['Sent'][person] = [message]

        elif sent_received == 'Received':
            if data['Messages']['Received'].__contains__(person):
                data['Messages']['Received'][person].append(message)
            else:
                data['Messages']['Received'][person] = [message]
        update = self.firebase.put(self.db_name + self.user_id + '/' + current_date, key, data)
        print("Added Message:", update)

    #should overwrite
    def addMood(self, moods_list, song_dict):
        data, key, current_date = self.retEntryDate()
        if moods_list != []:
            data['Mood']['Moods'] = moods_list
        if song_dict != {}:
            data['Mood']['Songs'] = song_dict
        update = self.firebase.put(self.db_name + self.user_id + '/' + current_date, key, data)
        print("Added Mood:",update)

    #Tasks
    def addTask(self, tasks_complete_list):
        data, key, current_date = self.retEntryDate()
        for task in tasks_complete_list:
            data['Tasks'][task]+=1

        update = self.firebase.put(self.db_name + self.user_id + '/' + current_date, key, data)
        print("Added Task:", update)
        
    def retrieveStats(self, current_date):

        retrieve = self.firebase.get(self.db_name + self.user_id, current_date)
        print("Retrieved:", retrieve)
        return retrieve
        
#Should create user stat at start up
'''
jackie = userStats(user_id, firebase, db_name)
'''

#Whenever a task is completed
'''
jackie.addTask([tasks[0], tasks[1], tasks[2]])
jackie.addMood(['angry', 'sad'], {'Never gonna give u up by rick astley': 'some spotify link'})
jackie.addMessage('Sent', 'P2', 'wassuppp')
'''

