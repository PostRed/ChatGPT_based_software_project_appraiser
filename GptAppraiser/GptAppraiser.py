import json
import os
import requests
import base64

from time import sleep
from tqdm import tqdm

class GptAppraiser:

    def __init__(self, config):
        self.config = config

    def localPredict(self, text):
        file_refact = open('GptAppraiser/refactoring.msg', 'r', encoding='utf-8')
        refact = file_refact.read()
        file_refact.close()
        ans = []
        for i in range(int(self.config['GptAppraiserSettings']['resending'])):
            response = send(self.config, text)

            response_status = {'done': False}
            while not response_status['done']:
                sleep(0.1)
                response_status = get(self.config, response['id'])

            for i in range(2):
                try:
                    x = response_status['response']['alternatives'][0]['message']['text']
                    ans.append(int(x))
                    break
                except Exception:
                    pass

                response = send(self.config, refact + response_status['response']['alternatives'][0]['message']['text'])

                response_status = {'done': False}
                while not response_status['done']:
                    sleep(0.1)
                    response_status = get(self.config, response['id'])
        return ans

    def remotePredict(self, text):

        url = 'http://158.160.109.151:7007'
        headers = {'Authorization': base64.b64encode(f"{self.config['GptAppraiserSettings']['login']}:{self.config['GptAppraiserSettings']['password']}".encode()).decode(),
                   'Content-Type': 'application/json'}
        data = {'type': 'predict', 'text': text}

        response = requests.post(url, headers=headers, json=data, timeout=150)
        id = json.loads(response.text)['id']
        sleep(10)
        data = {'type': 'check', "id": id}
        response = requests.post(url, headers=headers, json=data, timeout=150)
        print(response.text)
        while response.status_code != 200:
            sleep(1)
            response = requests.post(url, headers=headers, json=data, timeout=150)
            print(response.text)
        return list(map(int, json.loads(response.text)['response'][1:-1].split(', ')))


    def prompt(self, text):
        return {
            'modelUri': f"gpt://{self.config['GptAppraiserSettings']['x_folder_id']}/yandexgpt-lite",
            'completionOptions': {
                'stream': False,
                'temperature': 1e-5,
                'maxTokens': '1000'
            },
            'messages': [

                {
                    'role': 'user',
                    'text': text
                }
            ]
        }

    def send(self, text):
        response = requests.post('https://llm.api.cloud.yandex.net/foundationModels/v1/completionAsync',
                                 headers={
                                     'Content-Type': 'application/json',
                                     'Authorization': f"Api-Key {self.config['GptAppraiserSettings']['Api_Key']}",
                                     'x-folder-id': self.config['GptAppraiserSettings']['x_folder_id']},
                                 data=json.dumps(prompt(self.config, text)))
        return response.json()

    def get(self, id):
        response = requests.get('https://llm.api.cloud.yandex.net/operations/' + str(id),
                                headers={'Authorization': f"Api-Key {self.config['GptAppraiserSettings']['Api_Key']}"})
        return response.json()


    def predict(self, filename):


        fin = open(os.path.join('text_queries/', filename), 'r', encoding='utf-8')
        text = fin.read()
        if self.config['GptAppraiserSettings']['useServerAppraiser'] == 'true':
            ans = self.remotePredict(text)
        else:
            ans = self.localPredict(text)

        fin.close()
        return ans
