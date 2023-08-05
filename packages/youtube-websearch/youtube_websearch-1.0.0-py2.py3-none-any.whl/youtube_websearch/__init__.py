import urllib.request
import json

from bs4 import BeautifulSoup

base = "https://www.youtube.com/results?q="


def _get_webpage(url, useragent='Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'):
    """ get soup of the html content of a url
    :param url: url of the webpage
    :return: soup of the content form url, if it failes -> False
    """

    try:
        req = urllib.request.Request(url=url, headers={
            'User-Agent': useragent})
        resp = urllib.request.urlopen(req)
    except urllib.error.HTTPError:
        return False
    except urllib.error.URLError:
        return False

    if resp.code != 200:
        return False
    else:
        return BeautifulSoup(resp.read())


def plain_search(search_query, useragent='Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'):
    """ search youtube and get the raw json data back

    :param search_query: search string
    :return: raw ytInitialData form youtube
    """
    url = base + search_query.replace(" ", "+")

    soup = _get_webpage(url, useragent)

    script_tags = soup.findAll("script")

    search_json_data = None
    for script in script_tags:
        if script.string and "var ytInitialData = " == script.string[:20]:
            search_json_data = json.loads(script.string[20:-1]) # -1 is for removing ;

    if not search_json_data:
        print("No data found")
        return None

    return search_json_data


def messy_video_search(search_query, useragent='Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'):
    """ search youtube and get the raw video data back

    :param search_query: search string
    :return: raw video data from ytInitialData
    """
    search_data = plain_search(search_query, useragent)

    videos = search_data['contents']['twoColumnSearchResultsRenderer']['primaryContents']
    videos = videos['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']

    videos = filter(lambda v: 'videoRenderer' in v.keys(), videos)  # remove non videos
    videos = [video['videoRenderer'] for video in videos]

    return videos


def video_search(search_query, useragent='Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'):
    """ search youtube and get the cleaned up video data back

    :param search_query: search string
    :return: cleaned up video data
    """
    videos = messy_video_search(search_query, useragent)

    videos_cleaned = []
    for video in videos:
        videos_cleaned.append({
                            'videoId': video['videoId'],
                            'title': video['title']['runs'][0]['text'],
                            'publishedTimeText': video['publishedTimeText']['simpleText'],
                            'lengthText': video['lengthText']['accessibility']['accessibilityData']['label'],
                            'viewCountText': video['viewCountText']['simpleText'],
                           })
    return videos_cleaned
