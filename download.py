from __future__ import unicode_literals
import sqlite3
import urllib2
import time

import youtube_dl

BASE_URL = "https://www.youtube.com/watch?v=%s"
CONFIG_FILE_PATH = "config.json"

STATUS_NOT_DOWNLOADED = 0
STATUS_DOWNLOADED = 1
STATUS_DOWNLOAD_FAILED = 2


def download(conn, n, path):
    c = conn.cursor()
    c.execute("SELECT youtube_id, genre_id FROM song WHERE is_downloaded = ? LIMIT ?;", [STATUS_NOT_DOWNLOADED, n])
    metadata = c.fetchall()
    if len(metadata) == 0:
        return 0 # we are finished
    ids = [i for (i,g) in metadata]
    status_codes = []
    for (i, genre) in metadata:
        opts = {
            "outtmpl": path + ("/%s/" % genre) + "%(id)s.%(ext)s",
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                }]
            }
        with youtube_dl.YoutubeDL(opts) as ydl:
            try:
                ydl.download([BASE_URL % i])
            except urllib2.URLError, err:
                print "Faulty connection"
                status_codes.append(0)
            except:
                print "Could not download link"
                status_codes.append(2)
            else:
                status_codes.append(1)
    assert(len(ids) == len(status_codes))
    c.executemany("UPDATE song SET is_downloaded = ? WHERE youtube_id = ?", zip(status_codes, ids))
    conn.commit()
    return len([sc for sc in status_codes if sc == 1])

if __name__ == "__main__":
    with open(CONFIG_FILE_PATH) as f:
        config = json.load(f)
    conn = sqlite3.connect(config["database_path"])
    # download 10 at a time
    while (download(conn, 10, config["download_path"]) > 0):
        pass