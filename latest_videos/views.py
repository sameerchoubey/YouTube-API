from django.shortcuts import render
from django.http import HttpResponse
from apiclient.discovery import build
from django.core.exceptions import ObjectDoesNotExist
from .models import main_db
import time
import threading
import random

api_key = 'AIzaSyCJtkbrA7_U3SjJYHEAU5Ha0tZzOdsSqy8'
keyword = 'Premier League'

def fetch_from_youtube(keyword, api_key):
    while True:
        youtube = build('youtube', 'v3', developerKey=api_key)
        req = youtube.search().list(q=keyword, part='snippet', type='video', maxResults=50)
        res = req.execute()

        for item in res['items']:
            print(item['snippet']['title'])
            fetched_video_id = item['id']['videoId']
            found = True
            try:
                m = main_db.objects.get(video_id=fetched_video_id)
            except ObjectDoesNotExist:
                found = False

            if found:
                continue
            else:
                v_title = item['snippet']['title']
                v_description = item['snippet']['description']
                v_thumb_url = item['snippet']['thumbnails']['default']['url']
                v_published_date = item['snippet']['publishedAt'][:10]

                query = main_db(video_id=fetched_video_id, video_title=v_title,
                                description=v_description, published_date=v_published_date,
                                thumbnail_url=v_thumb_url)
                query.save()
        time.sleep(5)


t = threading.Thread(target=fetch_from_youtube, args=(keyword, api_key,))
t.daemon = True
# t.start()

# while True:
#     sameer()
#     time.sleep(5)


def index(request):
    m = main_db.objects.get(id=random.randint(1, 50))
    print(m.thumbnail_url)
    m = {"thumbnail": str(m.thumbnail_url), "title": str(m.video_title)}
    return render(request, 'index.html', {'m': m})
