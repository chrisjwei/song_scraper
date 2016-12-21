# Song Scraper
This is a scraper used to collect mp3 files from YouTube and cross reference them with iTunes to collect metadata about the song. This was used to collect clips of songs and find a genre id for each song. The songs were then passed through a machine learning algorithm in an attempt to classify genres.

## Dependencies
You will need to install [youtube-dl](https://github.com/rg3/youtube-dl) to actually download the mp3 files, and you will need FFMpeg installed on your machine to convert the downloaded video file to mp3.

## Configuration
config.json is used to load in different configurations

* database_path - path to your sqlite3 database file
* download_path - path to the folder to download your songs
* seed_genres - list of genres you want to seed your frontier with (must match iTunes' genre names)
* continue - whether or not to continue scraping, or start fresh
* scrape_song_limit - number of songs to scrape
* youtube_key - youtube search api key

## Database schemas
* song - stores scraped song links along with their metadata collected from iTunes
  * youtube_id - the youtube id of song
  * label - label of song
  * song_id - the iTunes id of the song
  * genre_id - the genre of the song
  * is_downloaded - flag for determining whether a song has been downloaded or not
* frontier - stores potential songs to explore
  * youtube_id - the youtube id of the potential song
  * label - the label of the potential song
* genre - genres scraped from iTunes
  * genre_id - the iTunes genre_id
  * parent_genre_id - the parent genre's id if it exists
  * genre_name - the iTunes genre name
  
## Exceptions
* 401 - Your youtube key is invalid or has exceeded its daily limit
* 403 - iTunes has some sort of hidden limit for the number of requests you can send it from a given IP. This works for me on one IP address but I get almost immediately throttled on another IP address. The mysteries of Apple...
