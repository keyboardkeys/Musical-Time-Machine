import requests
from bs4 import BeautifulSoup
from ytmusicapi import YTMusic

yt = YTMusic("browser.json")
playlists = [lists["title"] for lists in yt.get_library_playlists()]

if "New Playlist" not in playlists:
    yt.create_playlist("New Playlist", "A new playlist from an API")
    
print(playlists)

index = playlists.index("New Playlist")
print(index)

data = [lists["playlistId"] for lists in yt.get_library_playlists()]
playlistId = data[index]

# Scraping Bakeboard Hot 100
date = input(
    "Which year do you want to travel to? Type the date in this format "
    "YYYY-MM-DD: ")

url = f"https://appbrewery.github.io/bakeboard-hot-100/{date}"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
song_names = [tag.getText().strip() for tag in
              soup.select("h3.chart-entry__title")]

for song in song_names:
    # playlist = yt.get_playlist()
    print(f"Searching for song name: {song} ")
    search = yt.search(song, filter="songs", limit=1)
    try:
        videoId = search[0]["videoId"]
    except Exception as e:
        print(f"Couldn't find the music because of error: {e}")
    else:
        yt.add_playlist_items(playlistId, [videoId], duplicates=False)
        print(f"{song} has been added to the playlist")
