import urllib2
import json

def translate(search_text):
    response = urllib2.urlopen('http://api.giphy.com/v1/gifs/translate?s=%s&api_key=dc6zaTOxFJmzC' % search_text.replace(' ', '+'))
    data = json.load(response)['data']
    return data['images']['original']['url']

def search(search_text):
    response = urllib2.urlopen('http://api.giphy.com/v1/gifs/search?q=%s&limit=1&api_key=dc6zaTOxFJmzC' % search_text.replace(' ', '+'))
    data = json.load(response)['data']
    if len(data) > 0:
        return data[0]['images']['original']['url']
    else:
        raise Exception('The search query had no results')
