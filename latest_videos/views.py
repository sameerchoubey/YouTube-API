from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from apiclient.discovery import build
from django.core.exceptions import ObjectDoesNotExist
from .models import main_db
from django.core.paginator import Paginator
import time
import threading
import random

api_key = 'AIzaSyCJtkbrA7_U3SjJYHEAU5Ha0tZzOdsSqy8'
api_key_list = ['AIzaSyCJtkbrA7_U3SjJYHEAU5Ha0tZzOdsSqy8',
                'AIzaSyCp-442KSJuHyJv8k0YwRYd6LG_oeCWkxg',
                'AIzaSyCP_UQVrFtURgGwiQpSh7FXv68OfLVurjA',
                'AIzaSyCP_UQVrFtURgGwiQpSh7FXv68OfLVurjA',
                'AIzaSyAfwG4c9xak4ktEFSNAYK2fxQKLzMRGGJk',
                'AIzaSyCQpXJGFRBA7uWmicOf2iy065QMXqjOccw',
                'AIzaSyCvM6fyA3uTTyfXmoIOUStrdgG_QHobxOw',
                'AIzaSyAbi4YyRr2gQkOAytW4HD07Mt8hR-ctxtw',
                'AIzaSyCAOVUfWBln3bmWNNJEg4s00sOhxgsqCFU',
                'AIzaSyDcySmOFch4tzoRmfQlcDS2nybJWoxETq0']
keyword = 'Premier League'


def fetch_from_youtube(keyword, api_key):
    list_index = 0
    while True:
        youtube = build('youtube', 'v3', developerKey=api_key)
        req = youtube.search().list(q=keyword, part='snippet', type='video', maxResults=50)

        try:
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
        except:
            list_index = list_index + 1
            list_index = list_index % 5
            api_key = api_key_list[list_index]

        time.sleep(5)


t = threading.Thread(target=fetch_from_youtube,
                     args=(keyword, api_key_list[0],))
t.daemon = True
t.start()


def index(request):
    content = main_db.objects.order_by('-published_date')
    paginator = Paginator(content, 5)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    context = {
        'content': content
    }
    return render(request, 'index.html', context)


# API Function that will returns data in JSON Format.
def index_api(request):
    content = main_db.objects.order_by('-published_date').values()
    context = {
        'content': list(content)
    }
    return JsonResponse(context)
