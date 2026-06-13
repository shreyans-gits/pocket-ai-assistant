import webbrowser as wb
import wikipedia
import urllib.parse


class SearchModule:
    def __init__(self):
        self.browser = wb

    def open_browser(self, url: str):
        self.browser.open_new(url)

    def search(self, query):
        url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
        self.open_browser(url)

    def watch(self, query):
        url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)
        self.open_browser(url)

    def getWiki(self, query):
        try:
            result = wikipedia.summary(query, sentences=2)
            return result
        except Exception:
            return "Could not find query"