from http.server import BaseHTTPRequestHandler, HTTPServer
import base64
import json
import requests
import os
from time import sleep
from multiprocessing import Process

x_folder_id = 'b1gba0ng25v7j8nff8aa'
Api_Key = 'AQVNx_E26gmZ36b3TzSCLk03p5qkqaWwEqeh9PgD'

users = {
    'ServerConnector1': 'Passw0rd!'
}

class ServerAppraiser(BaseHTTPRequestHandler):

    @staticmethod
    def prompt(text):
        return {
            'modelUri': f"gpt://{x_folder_id}/yandexgpt-lite",
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

    @staticmethod
    def sendToGpt(text):
        response = requests.post('https://llm.api.cloud.yandex.net/foundationModels/v1/completionAsync',
                                 headers={
                                     'Content-Type': 'application/json',
                                     'Authorization': f"Api-Key {Api_Key}",
                                     'x-folder-id': x_folder_id},
                                 data=json.dumps(ServerAppraiser.prompt(text)))
        return response.json()

    @staticmethod
    def getFromGpt(id):
        response = requests.get('https://llm.api.cloud.yandex.net/operations/' + str(id),
                                headers={'Authorization': f"Api-Key {Api_Key}"})
        return response.json()

    @staticmethod
    def predict(data):
        print("predict start")
        file_refact = open('refactoring.msg', 'r', encoding='utf-8')
        refact = file_refact.read()
        file_refact.close()
        ans = []

        for i in range(2):
            response = ServerAppraiser.sendToGpt(data['text'])

            response_status = {'done': False}
            while not response_status['done']:
                sleep(0.1)
                response_status = ServerAppraiser.getFromGpt(response['id'])

            for i in range(2):
                try:
                    x = response_status['response']['alternatives'][0]['message']['text']
                    ans.append(int(x))
                    break
                except Exception:
                    pass

                response = ServerAppraiser.sendToGpt(refact + response_status['response']['alternatives'][0]['message']['text'])

                response_status = {'done': False}
                while not response_status['done']:
                    sleep(0.1)
                    response_status = ServerAppraiser.getFromGpt(response['id'])
        return ans

    def do_POST(self):
        try:
            authorization_data = base64.b64decode(self.headers['Authorization']).decode()
            login, password = authorization_data.split(':')

            if login not in users or users[login] != password:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'Wrong login or password')
                return

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            data = json.loads(post_data.decode())

            response_data = {'response': str(ServerAppraiser.predict(data))}
            response = json.dumps(response_data)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response.encode())

        except:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Bad data')


def run(server_class, handler_class, port):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    p1 = Process(target=run, args=(HTTPServer, ServerAppraiser, 7009), daemon=True)
    p2 = Process(target=run, args=(HTTPServer, ServerAppraiser, 7008), daemon=True)
    p1.start()
    p2.start()
    p1.join()
    p2.join()