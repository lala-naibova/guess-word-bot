import requests


class WordGenerator:

    def __init__(self):
        self.key = None
        self._update_key()

    def _update_key(self):
        response = requests.get('https://random-word-api.herokuapp.com/key?')
        self.key = response.text

    def generate_word(self):
        url = 'https://random-word-api.herokuapp.com/word?key={}&number=1'.format(self.key)
        response = requests.get(url)
        result = response.json()[0]
        if result == 'w':
            self._update_key()
            return self.generate_word()
        return result

