import json
import os
import requests

from time import sleep
from tqdm import tqdm

def prompt(config, text):
    return {
        'modelUri': f"gpt://{config['GptAppraiserSettings']['x_folder_id']}/yandexgpt-lite",
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

def send(config, text):
    response = requests.post('https://llm.api.cloud.yandex.net/foundationModels/v1/completionAsync',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': f"Api-Key {config['GptAppraiserSettings']['Api_Key']}",
                                 'x-folder-id': config['GptAppraiserSettings']['x_folder_id']},
                             data=json.dumps(prompt(config, text)))
    return response.json()

def get(config, id):
    response = requests.get('https://llm.api.cloud.yandex.net/operations/' + str(id),
                            headers={'Authorization': f"Api-Key {config['GptAppraiserSettings']['Api_Key']}"})
    return response.json()


def GptAppraiser(config, filename):
    file_refact = open('GptAppraiser/refactoring.msg', 'r', encoding='utf-8')
    refact = file_refact.read()
    file_refact.close()
    ans = []
    fin = open(os.path.join('text_queries/', filename), 'r', encoding='utf-8')
    text = fin.read()
    for i in range(int(config['GptAppraiserSettings']['resending'])):
        response = send(config, text)

        response_status = {'done': False}
        while not response_status['done']:
            sleep(0.1)
            response_status = get(config, response['id'])

        for i in range(2):
            try:
                x = response_status['response']['alternatives'][0]['message']['text']
                ans.append(int(x))
                break
            except Exception:
                pass

            response = send(config, refact + response_status['response']['alternatives'][0]['message']['text'])

            response_status = {'done': False}
            while not response_status['done']:
                sleep(0.1)
                response_status = get(config, response['id'])

    fin.close()
    return ans