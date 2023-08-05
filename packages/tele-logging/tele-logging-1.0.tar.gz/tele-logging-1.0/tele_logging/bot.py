import requests


class Bot:
    def __init__(self, token):
        self.token = token
        self.api = f'https://api.telegram.org/bot{token}/'
        self.chat_id = self.get_chat_id()


    def send_message(self, text):
        params = {'chat_id': self.chat_id, 'text': text}
        method = 'sendMessage'
        response = requests.post(self.api + method, params).json()
        return response


    def get_chat_id(self):
        return self.get_updates()['result'][0]['message']['chat']['id']


    def get_updates(self, limit=1):
        method = 'getUpdates'
        params = {'limit': limit}
        response = requests.post(self.api + method, params).json()
        return response
