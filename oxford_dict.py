import requests


class DefinitionProvider:

    language = 'en'

    base_url = 'https://od-api.oxforddictionaries.com:443/api/v2'

    def __init__(self, api_key, app_id):
        self.api_key = api_key
        self.app_id = app_id

    def get_definition(self, word):
        word = word.lower()
        url = self.base_url + '/entries/' + self.language + '/' + word
        response = requests.get(url, headers={'app_id': self.app_id, 'app_key': self.api_key})
        payload = response.json()
        definition = payload['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
        hint = payload['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['shortDefinitions'][0]
        audio_url = payload['results'][0]['lexicalEntries'][0]['pronunciations'][0]['audioFile']
        return {
            'definition': definition,
            'hint': hint,
            'audio_url': audio_url
        }
