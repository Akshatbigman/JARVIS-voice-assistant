import webbrowser, urllib, re
import urllib.parse
import urllib.request

domain = input("Enter the song name: ")
song = urllib.parse.urlencode({"search_query" : domain})
print("Song" + song)

result = urllib.request.urlopen("http://www.youtube.com/results?" + song)
print(result)

search_results = re.findall(r'href=\"\/watch\?v=(.{4})', result.read().decode())
print(search_results)

url = "http://www.youtube.com/watch?v="+str(search_results)

webbrowser.open_new(search_results)