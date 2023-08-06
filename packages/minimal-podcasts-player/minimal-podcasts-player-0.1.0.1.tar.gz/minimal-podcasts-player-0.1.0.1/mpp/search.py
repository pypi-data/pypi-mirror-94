from urllib.request import urlopen
import urllib.parse
from PyQt5.QtCore import pyqtSignal, QThread, QVariant
import json


class itunes(QThread):
    data = pyqtSignal(QVariant)
    baseUrl = 'https://itunes.apple.com/search'

    def __init__(self, terms):
        super().__init__()
        self.terms = terms

    def run(self):
        data = {}
        data['term'] = 'energy power'
        data['media'] = 'podcast'
        # data['country'] = 'ES'
        # data['language'] = 'Python'
        url_values = urllib.parse.urlencode(data)
        full_url = self.baseUrl + '?' + url_values
        print(full_url)
        with urlopen(full_url) as response:
            rawData = response.read().decode('utf-8')
            data = json.loads(rawData)
            for result in data['results']:
                if 'feedUrl' in result:
                    print(result['trackName'])
                    print(result['feedUrl'])
            # self.data.emit(response.read())


thread = itunes('')
#thread.podcast.connect(self.addPCList)
thread.start()
