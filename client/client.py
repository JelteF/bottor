#!/usr/bin/env python
from pprint import pprint
import requests
import json
import psutil
import threading
import time

URL = 'http://localhost:5000'
json_header = {'content-type': 'application/json'}
p = psutil.Process()
have_to_wait = False

default_task = {
    'id': 2,
    'rows': [
        {
            'number': 1,
            'sequence': [1, 4, 5]
        }
    ],
    'columns': [
        {
            'number': 1,
            'sequence': [1, 3, 2]
        }
    ]
}

def main():
    p.cpu_affinity([0])
    psutil.cpu_percent()
    p.cpu_percent()

    _id = handshake()

    do_every(0.5, send_cpu_ping, _id)

    while(1):
        print('Requesting new task')
        task = request_task(_id)
        print('Received task')
        print('Calculating answer')
        answer = calculate_answer(task)
        print('Calculated answer')


        print('Sending answer')
        send_result(answer)
        print('Sent answer')



"""
http://stackoverflow.com/a/11488902
"""
def do_every (interval, worker_func, *args, **kwargs):
    new_args = [interval, worker_func]
    temp = new_args.extend(args)
    threading.Timer(interval, do_every, new_args, kwargs).start();

    worker_func(*args, **kwargs)

def handshake():
    data = json.dumps({'secret': 'ILIKETURTLES'})
    r = requests.post(URL + '/api/peer', data=data, headers=json_header)
    return r.json()['id']


def request_task(_id):
    return requests.get(URL + '/api/task/request_task/' + str(_id)).json()


def send_result(answer):
    data = json.dumps(answer)
    requests.post(URL + '/api/task/send_result', data=data, headers=json_header)


def send_cpu_ping(_id):
    load, own_load = get_load()

    data = json.dumps({'load': load, 'own_load': own_load})
    requests.post(URL + '/api/peer/ping/' + str(_id),
                  data=data, headers=json_header)


def get_load():
    load = psutil.cpu_percent()
    own_load = p.cpu_percent()
    if load > 60:
        have_to_wait = True
    print(load, own_load)
    return load, own_load


def calculate_answer(task):
    answer = {
        'id': task['id'],
        'results': [
        ]
    }

    for row_num, r in task['rows'].items():
        for col_num, c in task['columns'].items():
            answer['results'].append({'row': int(row_num),
                                      'col': int(col_num)})
            total = 0

            for i in range(len(r)):
                if have_to_wait:
                    print('waiting')
                    time.sleep(1)
                total += r[i] * c[i]

            answer['results'][-1]['value'] = total

    print('Finished task: ' + str(task['id']))
    return answer


if __name__ == '__main__':
    main()
