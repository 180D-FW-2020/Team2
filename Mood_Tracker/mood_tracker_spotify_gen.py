import numpy as np
import requests
import json

#Dont' change the CLIENT_ID and CLIENT_SECRET. The user will enter their user_id later as an input.
CLIENT_ID = "1b78b7d9ddc947819403aa0a8b5fde21"
CLIENT_SECRET = "caba3930090243d19ee50fd30d234a9f"
user_id = ""

def pretty_string_matrix(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    return '\n'.join(table)

def prompting_genre_input(question):
    seed_genres = input(question)
    while True:
        if seed_genres not in genre_list:
            seed_genres = input("Please enter a genre from the list ==>")
            continue
        else:
            break
    return seed_genres

def prompting_int_input(question, down_scale):
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

#This token only works for getting recommended songs
def get_access_token(CLIENT_ID, CLIENT_SECRET):
    #Creating access token, not authorizing user. Not sure if this works

    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'scope': 'playlist-modify-private',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    token = auth_response_data['access_token']
    return token

def get_genre_list(token):
    genre_endpoint =  "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    response = requests.get(genre_endpoint,
                   headers={"Content-Type":"application/json",
                            "Authorization":f"Bearer {token}"})
    json_response = response.json()
    return json_response['genres']

def get_song_recs(token, limit, market, seed_genres, target_danceability, target_energy, target_popularity, target_valence):
    song_url_list = []
    uris = []
    endpoint_url = "https://api.spotify.com/v1/recommendations?"
    query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}'
    query+= f'&target_energy={target_energy}'
    query+= f'&target_danceability={target_danceability}'
    query+= f'&target_valence{target_valence}'
    query+=f'&target_popularity{int(target_popularity)}'
    response = requests.get(query,
                   headers={"Content-Type":"application/json",
                            "Authorization":f"Bearer {token}"})
    json_response = response.json()
    if response.status_code != 200:
        print(str(response.status_code) + ": Could not generate songs")
        return

    print('Recommended Songs:')
    for i,j in enumerate(json_response['tracks']):
        first_col = f"{i+1}) \"{j['name']}\" by {j['artists'][0]['name']}"
        second_col = f"{j['external_urls']['spotify']}"
        song_url_list.append([first_col, second_col])

        uris.append(j['uri'])
    print(pretty_string_matrix(song_url_list))
    return uris
    #print(f"{i+1}) \"{j['name']}\" by {j['artists'][0]['name']} {j['external_urls']['spotify']}")

def create_playlist(user_id, token, uris):
    endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"

    request_body = json.dumps({
              "name": "Generated playlist",
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



#Start
token = get_access_token(CLIENT_ID, CLIENT_SECRET)
genre_list = get_genre_list(token)
genre_table = np.array_split(genre_list, len(genre_list)/3) #3 columns

seed_genres = prompting_genre_input("What genre are you in the mood today for?\n" + pretty_string_matrix(genre_table) +'\n ==> ' )

#Rest of playlist seeds
target_energy = prompting_int_input("How much ENERGY do you have today on a scale of 1-10? ",10)
target_valence = prompting_int_input("How POSITIVE do you feel today on a scale of 1-10? ",10)
target_popularity = prompting_int_input("How POPULAR would you like your songs to be on a scale of 1-10 ",1)*10
target_danceability = prompting_int_input("How much would you like to DANCE today on a scale of 1-10? ", 10)
limit=10
market="US"
uris = get_song_recs(token, limit, market, seed_genres, target_danceability, target_energy, target_popularity, target_valence)
user_id = input("Enter your spotify user id if you would like to create a playlist on your spotify. If you don't want to, just press Enter ==> ")
if user_id == "":
    #Just end script if they don't want to make a playlist
    quit()
else:
    token = input("If you would like to generate a playlist, go to https://developer.spotify.com/console/post-playlists/ to enter your spotify id and 'Get Token' under the 'OAth Token' tab. Select the scope to be 'playlist-modify-private' and generate the token. Once you have done that, copy and paste the token here ")
    #token= "BQAYsVoec6vo45Pl2vggVWOFY7KA4FLPsgNVqTqNDtgnds6TUYTJxcMzs8gdKdT1xCFQRi4c9p8Xozg2yDMCNcey6DPMwFzdvvxZkYKI591ssnRJlMWAYHAytKn5A-O9633-5WbO0MomJUCG9ouDWm-EemlYfmnjSzmVB3eAvaOklg"
    playlist_id = create_playlist(user_id, token, uris)
