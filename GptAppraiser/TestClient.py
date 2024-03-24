import requests
import base64
from time import sleep

def send_request(login, password):
    with open('C:/HSE/ChatGPT_based_software_project_appraiser/text_queries/test') as fin:
        url = 'http://158.160.109.151:7007'
        headers = {'Authorization': base64.b64encode(f'{login}:{password}'.encode()).decode(),
                   'Content-Type': 'application/json'}
        data = {'type': 'predict', 'text': fin.read()}

        response = requests.post(url, headers=headers, json=data, timeout=150)

        print(response.status_code)
        print(response.text)

def get_ans(login, password):

    url = 'http://158.160.109.151:7007'
    headers = {'Authorization': base64.b64encode(f'{login}:{password}'.encode()).decode(),
               'Content-Type': 'application/json'}
    data = {'type': 'check', "id": 2}

    response = requests.post(url, headers=headers, json=data, timeout=150)

    print(response.status_code)
    print(response.text)


if __name__ == '__main__':
    login = 'aboba'
    password = 'Passw0rd!'
    #send_request(login, password)
    #sleep(2)
    get_ans(login, password)