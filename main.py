import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import music_tag
import shutil
import time
import random
import json

json_file = open('main.json')
data = json.load(json_file)

input_folder = data['input_folder']
processing_folder = data['processing_folder']
output_folder = data['output_folder']
minimum_time_between_two_songs = data['minimum_time_between_two_songs']
maximum_time_between_two_songs = data['maximum_time_between_two_songs']
spotify_client_id = data['spotify_client_id']
spotify_client_secret = data['spotify_client_secret']

minimum_time_between_two_songs = int(minimum_time_between_two_songs)
maximum_time_between_two_songs = int(maximum_time_between_two_songs)
json_file.close()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(spotify_client_id,spotify_client_secret))




def music_file_name(file_name):
    song_file = os.path.basename(file_name)
    print(os.path.splitext(song_file)[0])
    song_file_name = os.path.splitext(song_file)[0]
    results = sp.search(q=song_file_name, limit=1)


    for idx, track in enumerate(results['tracks']['items']):
        song_file_picture = "output"+".png"
        command_input = "wget " + track['album']['images'][0]['url'] + ' -O "' + song_file_picture + '"'
        print(command_input)
        os.system(command_input)
        f = music_tag.load_file(song_file)
        print("********************************")
        print("Title:- " + track['name'])
        title_item = f['title']
        f['title'] = track['name']
        artist_run = True
        i = 0
        artist_names = ""
        while artist_run:
            try:
                artist_name = track['album']['artists'][i]['name']
                print("Artists Name:- " + artist_name)
                i +=1
                artist_names+= artist_name + " "
            except:
                artist_run = False

        print(track['album']['release_date'])
        album_type = track['album']['album_type']
        print("artist_names")
        print(artist_names)
        f['artist'] = artist_names

        if(album_type=='album'):
            print("Album")
            print("Album Name:- "+ track['album']['name'])
            print("Album Name:- "+ track['album']['release_date'])
            f['album'] = track['album']['name']
            f['year'] = track['album']['release_date']
        else:
            f['album'] = track['album']['name']
            f['year'] = track['album']['release_date']
            print("Song Release Date:- " + track['album']['release_date'])
        print("Image:- " + track['album']['images'][0]['url'])


        with open(song_file_picture, 'rb') as img_in:
            f['artwork'] = img_in.read()

        f.save()
        os.remove(song_file_picture)



if __name__ == "__main__":
    for (root, dirs, file) in os.walk(input_folder):
        for f in file:
            #print(f)
            input_file_path = input_folder + "/" + f
            processing_file_path = f
            shutil.move(input_file_path,processing_file_path)
            music_file_name(processing_file_path)
            output_file_path = output_folder + "/" + f
            shutil.move(processing_file_path,output_file_path)
            time.sleep(random.randint(minimum_time_between_two_songs,maximum_time_between_two_songs))




