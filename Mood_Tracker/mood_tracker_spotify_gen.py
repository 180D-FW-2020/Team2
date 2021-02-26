import numpy as np
import requests
import json

from selenium import webdriver 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#Dont' change the CLIENT_ID and CLIENT_SECRET. The user will enter their user_id later as an input.
CLIENT_ID = "1b78b7d9ddc947819403aa0a8b5fde21"
CLIENT_SECRET = "caba3930090243d19ee50fd30d234a9f"
moods = ["Happy/Excited", "Angry/Frustrated", "Unmotivated", "Disappointed", "Sad", "Stressed"]
limit=10
market="US"

class moodTracker:
    def __init__(self, spotify_user_id = ''):
        self.spotify_user_id = spotify_user_id
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET
        self.playlist_name = "Generated playlist!"
        self.access_token = ''
        self.token = ''
        self.uris = []
        self.seed_genres = []
        self.target_danceability = 0
        self.target_energy = 0
        self.target_popularity = 0
        self.target_valence = 0
        self.playlist_id = ''
        self.uris = []
        self.song_dict = {}
        self.mood_list = []

    def get_token(self, user_id):
        token = ""
        browser = webdriver.Chrome()
        browser.get("https://developer.spotify.com/console/post-playlists/")
        
        id_field = browser.find_element_by_name("user_id")
        id_field.send_keys(user_id)

        token_id = browser.find_element_by_id("oauth-input")
        token_val = token_id.get_attribute("value")

        enter_button = browser.find_element_by_class_name("btn-green")
        enter_button.click()

        scope_button = browser.find_element_by_xpath("//*[contains(text(), 'playlist-modify-private')]") # locate the dropdown elem
        browser.implicitly_wait(30)
        scope_button.click()

        request_button = browser.find_element_by_class_name("btn-primary")
        browser.implicitly_wait(10)
        request_button.click()
        
        try:
            element_present = EC.presence_of_element_located((By.ID, 'oauth-input'))
            WebDriverWait(browser, 60).until(element_present)
            token_field = browser.find_element_by_id("oauth-input")
            token = token_field.get_attribute("value")
        except:
            print("timed out waiting for token")

        return token
    
    def pretty_string_matrix(self, matrix):
        s = [[str(e) for e in row] for row in matrix]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        return '\n'.join(table)

    def prompting_genre_input(self, genre_list, question):
        seed_genres = input(question)
        while True:
            if seed_genres not in genre_list:
                seed_genres = input("Please enter a genre from the list ==>")
                continue
            else:
                break
        return seed_genres

    def prompting_int_input(self, question, down_scale):
        while True:
            try:
                ret = int(input(question))
            except ValueError:
                print("Please enter an integer from 1-10")
                #better try again... Return to the start of the loop
                continue
            if ret <1 or ret>10:
                print("Please enter an integer from 1-10")
                continue
            else:
                #Accepted
                break
        return ret/down_scale

    def prompting_mood_input(self,question):
        mood_list = []
        while True:
            try:
                ret_string = input(question)
                ret_list = list(ret_string.split(','))
                ret_int = list(map(int, ret_list))
            except ValueError:
                print("Please enter integers from 0-5")
                #better try again... Return to the start of the loop
                continue
            else:
                #Accepted
                break
        for i in ret_int:
            mood_list.append(moods[i])
        print(mood_list)
        return mood_list
    #This token only works for getting recommended songs
    def get_access_token(self):
        #Creating access token, not authorizing user. Not sure if this works

        AUTH_URL = 'https://accounts.spotify.com/api/token'

        # POST
        auth_response = requests.post(AUTH_URL, {
            'grant_type': 'client_credentials',
            'scope': 'playlist-modify-private',
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
        })

        # convert the response to JSON
        auth_response_data = auth_response.json()

        # save the access token
        access_token = auth_response_data['access_token']
        return access_token

    def get_genre_list(self, access_token):
        genre_endpoint =  "https://api.spotify.com/v1/recommendations/available-genre-seeds"
        response = requests.get(genre_endpoint,
                    headers={"Content-Type":"application/json",
                                "Authorization":f"Bearer {access_token}"})
        json_response = response.json()
        return json_response['genres']

    def get_song_recs(self, access_token, seed_genres, target_danceability, target_energy, target_popularity, target_valence):
        song_url_list = []
        uris = []
        song_dict = {}
        endpoint_url = "https://api.spotify.com/v1/recommendations?"
        query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}'
        query+= f'&target_energy={target_energy}'
        query+= f'&target_danceability={target_danceability}'
        query+= f'&target_valence{target_valence}'
        query+=f'&target_popularity{int(target_popularity)}'
        response = requests.get(query,
                    headers={"Content-Type":"application/json",
                                "Authorization":f"Bearer {access_token}"})
        json_response = response.json()
        if response.status_code != 200:
            print(str(response.status_code) + ": Could not generate songs")
            return

        print('Recommended Songs:')
        for i,j in enumerate(json_response['tracks']):
            song_number_index = f"{i+1}) "
            first_col = f"{j['name']} by {j['artists'][0]['name']}"
            # first_col = f"{i+1}) \"{j['name']}\" by {j['artists'][0]['name']}"
            second_col = f"{j['external_urls']['spotify']}"
            song_url_list.append([song_number_index + first_col, second_col])
            song_dict[first_col] = second_col
            uris.append(j['uri'])
        print(self.pretty_string_matrix(song_url_list))
        return uris, song_dict
        #print(f"{i+1}) \"{j['name']}\" by {j['artists'][0]['name']} {j['external_urls']['spotify']}")

    def create_playlist(self, spotify_user_id, token, uris, playlist_name):
        endpoint_url = f"https://api.spotify.com/v1/users/{spotify_user_id}/playlists"

        request_body = json.dumps({
                "name": playlist_name,
                "description": "My first programmatic playlist, yooo!",
                "public": False
                })
        response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json",
                                "Authorization":f"Bearer {token}"})

        if response.status_code != 201:
            print(str(response.status_code) + ": Could not create playlist. Invalid generated token or username")
            return
        url = response.json()['external_urls']['spotify']

        #Fill playlist
        playlist_id = response.json()['id']

        endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        request_body = json.dumps({
                "uris" : uris
                })
        response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json",
                                "Authorization":f"Bearer {token}"})

        print(response.status_code)
        if response.status_code != 201:
            print("Could not fill playlist")
            return
        print("Your Spotify playlist is available here: " + url)
        return playlist_id

    #Run the following as driver code
    def run_task(self):
        self.access_token = self.get_access_token()
        self.genre_list = self.get_genre_list(self.access_token)
        self.genre_table = np.array_split(self.genre_list, len(self.genre_list)/3) #3 columns
        
        #need to allow user to add multiple genres
        self.seed_genres = self.prompting_genre_input(self.genre_list, "What genre are you in the mood today for?\n" + self.pretty_string_matrix(self.genre_table) +'\n ==> ' )
        
        #prompt for target seeds
        self.target_energy = self.prompting_int_input("How much ENERGY do you have today on a scale of 1-10? ",10)
        self.target_valence = self.prompting_int_input("How POSITIVE do you feel today on a scale of 1-10? ",10)
        self.target_popularity = self.prompting_int_input("How POPULAR would you like your songs to be on a scale of 1-10 ",1)*10
        self.target_danceability = self.prompting_int_input("How much would you like to DANCE today on a scale of 1-10? ", 10)

        #prompt for moods. User will input 1,2,5 or something
        self.mood_list = self.prompting_mood_input("Select your moods from today: 0(Happy/Excited), 1(Angry/Frustrated), 2(Unmotivated), 3(Disappointed), 4(Sad), 5(Stressed): ")
        #get song rec list
        self.uris, self.song_dict = self.get_song_recs(self.access_token, self.seed_genres, self.target_danceability, self.target_energy, self.target_popularity, self.target_valence)
        
        #get spotify uesr name
        self.spotify_user_id = input("Enter your spotify user id if you would like to create a playlist on your spotify. If you don't want to, just press Enter ==> ")
        if self.spotify_user_id == "":
            #Just return if they don't want to make a playlist
            return
        else:
            self.playlist_name = input("Enter the playlist name =>")
            self.token = self.get_token(self.spotify_user_id)
            self.playlist_id = self.create_playlist(self.spotify_user_id, self.token, self.uris, self.playlist_name)

        
'''Run program by just calling run_task()'''
moodTracker = moodTracker()
moodTracker.run_task()