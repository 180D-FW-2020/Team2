from firebase import firebase
from datetime import datetime
import json
#pip install git+https://github.com/ozgur/python-firebase

#user_id = 'jackielam'
db_name = 'team2-4ffc1/stats/'
firebase = firebase.FirebaseApplication("https://team2-4ffc1-default-rtdb.firebaseio.com/", None)
STRETCHING = 0
BREATHING = 1
TALKING_TO_FRIENDS = 2
RECEIVED = 3
SENT = 4

tasks = {STRETCHING: 'stretching', BREATHING: 'breathing', TALKING_TO_FRIENDS: 'talking to friends', RECEIVED: 'Received', SENT: 'Sent'}

class userStats:
    def __init__(self, user_id = '', firebase = firebase, db_name = db_name):
        self.user_id = user_id
        self.firebase = firebase
        self.db_name = db_name
        self.initial_data = { 

            'Tasks': {
                tasks[STRETCHING]: 0,
                tasks[BREATHING]: 0,
                tasks[TALKING_TO_FRIENDS]: 0
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
                'Songs' : ['song by artist']
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
        sent_received_string = tasks[sent_received]
        if sent_received_string == 'Sent':
            if data['Messages']['Sent'].__contains__(person):
                data['Messages']['Sent'][person].append(message)
            else:
                data['Messages']['Sent'][person] = [message]

        elif sent_received_string == 'Received':
            if data['Messages']['Received'].__contains__(person):
                data['Messages']['Received'][person].append(message)
            else:
                data['Messages']['Received'][person] = [message]
        update = self.firebase.put(self.db_name + self.user_id + '/' + current_date, key, data)
        print("Added Message:", update)

    #should overwrite
    def addMood(self, moods_list, song_dict):
        data, key, current_date = self.retEntryDate()
        
        if song_dict != []:
            song_list = []
            for song_key, value in song_dict.items():
                song_list.append(song_key + ',' + value)
            data['Mood']['Songs'] = song_list

            # data['Mood']['Songs'] = song_dict
            # for song_key,value in song_dict.items():
            #     data['Mood']['Songs'][song_key] = value
            #     print("DATA", song_key, value)
            #     update = self.firebase.put(self.db_name + self.user_id + '/' + current_date + '/' + key + '/' + "Mood" , "Songs", {song_key:value})
            update = self.firebase.put(self.db_name + self.user_id + '/' + current_date, key, data)


        if moods_list != []:
            data['Mood']['Moods'] = moods_list
            update = self.firebase.put(self.db_name + self.user_id + '/' + current_date, key, data)

        print("Added Mood:",update)

    #Tasks
    def addTask(self, tasks_complete_list):
        data, key, current_date = self.retEntryDate()
        for task in tasks_complete_list:
            task_string = tasks[task]
            data['Tasks'][task_string]+=1

        update = self.firebase.put(self.db_name + self.user_id + '/' + current_date, key, data)
        print("Added Task:", update)
        
    def retrieveStats(self, current_date):

        retrieve = self.firebase.get(self.db_name + self.user_id, current_date)
        print("Retrieved:", retrieve)
        return retrieve

#Should create user stat at start up

# jackie = userStats('jackielam')
# jackie.addMood(['angry', 'sad'], ['Sail - Unlimited Gravity Remix by AWOLNATION', 
# 'Sugar High by Approaching Nirvana', 
# 'Crystallize by Lindsey Stirling', 
# 'Need Your Heart (feat. Kai) by Adventure Club', 
# 'Rabbit Whore - Original Mix by Savant',
# 'Bullet Train (feat. Joni Fatora) by Stephen Swartz',
# 'One Day (Vandaag) - Radio Edit by Bakermat',
# 'You - Tiësto vs. Twoloud Radio Edit by Galantis',
# 'Staying (DotEXE Remix) by Koda',
# 'Finale (feat. Nicholas Petricca) by Madeon'
# ])

#Whenever a task is completed
'''
jackie.addTask([tasks[0], tasks[1], tasks[2]])
jackie.addMood(['angry', 'sad'], {'Never gonna give u up by rick astley': 'some spotify link'})
jackie.addMessage('Sent', 'P2', 'wassuppp')
'''

