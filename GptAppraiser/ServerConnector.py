from http.server import BaseHTTPRequestHandler, HTTPServer
import base64
import json
import requests
import threading
from queue import Queue
users = {
    'aboba' : 'Passw0rd!'
}


class LoadBalancer:

    def __init__(self, servers):
        self.servers = servers
        self.request_queue = Queue()
        self.lock = threading.Lock()
        self.cur_id = 0
        self.results = {}


    def start(self):
        for server in self.servers:
            threading.Thread(target=self.worker, args=(server,)).start()

    def worker(self, server_url):
        while True:
            request_data = self.request_queue.get()
            headers = {'Authorization': base64.b64encode(f'ServerConnector1:Passw0rd!'.encode()).decode(),'Content-Type': 'application/json'}
            response = requests.post(server_url, headers=headers, data=request_data['data'], timeout=150)

            self.results[request_data['id']] = response
            self.request_queue.task_done()

    def distribute_request(self, headers, data):
        with self.lock:
            self.cur_id += 1
            self.request_queue.put({'headers': headers, 'data': data, 'id': self.cur_id})
            return self.cur_id

class LoadBalancerRequestHandler(BaseHTTPRequestHandler):
    load_balancer = LoadBalancer(['http://localhost:7008'])

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            authorization_data = base64.b64decode(self.headers['Authorization']).decode()
            login, password = authorization_data.split(':')

            if login not in users or users[login] != password:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'Wrong login or password')
                return

            data = json.loads(post_data.decode())
            if data['type'] == 'predict':
                id = LoadBalancerRequestHandler.load_balancer.distribute_request(self.headers, post_data)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({'id' : id}).encode())
                return
            if data['type'] == 'check' and int(data['id']) in  LoadBalancerRequestHandler.load_balancer.results:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(LoadBalancerRequestHandler.load_balancer.results[int(data['id'])].content)
                LoadBalancerRequestHandler.load_balancer.results.pop(int(data['id']))
                return
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'Bad data')
        except:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'Bad data')


def run(server_class=HTTPServer, handler_class=LoadBalancerRequestHandler, port=7007):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting load balancer on port {port}...')
    LoadBalancerRequestHandler.load_balancer.start()
    httpd.serve_forever()

if __name__ == '__main__':
    run()