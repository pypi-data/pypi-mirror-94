# youtube websearch libary

* no api key required
* no api limit

search through via web scraping

if you know how to test something like this, feel free to make as issue/pull request

### Example Usage
open we will rock you in a webbrowser:

```python3
import youtube_websearch as yt
import webbrowser

yt_basis = "https://www.youtube.com/watch?v="

search_results = yt.search('we will rock you')
# search_results = yt.search('we will rock you', useragent="something")  # you can set your own useragent
videoId = search_results[0]["videoId"]

webbrowser.open(yt_basis + videoId)
```

###
```bash
pip install youtube-websearch
```

### this libary provides multiple depths of search:

#### video_search

This function only returns the videos with this data:
* videoId
* title
* publishedTimeText
* lengthText
* viewCountText

if you need more videodata like thumbnails etc. use `messy_video_search`
if you think there is data this function should return, feel free and make a issue/pull request

#### messy_video_search

This functions returns the plain video search data. 

if you need meta information about your search use `plain_search`

#### plain_search

This function returns the whole search json. its a very messy thing with a lot of irrelevant data

