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
    'start_row': 1,
    'start_col': 4,

    'matrixA': [[1, 4, 5]],
    'matrixB': [[1, 3, 2]],
}


def main():
    # p.cpu_affinity([0])
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


def do_every(interval, worker_func, *args, **kwargs):
    """
    http://stackoverflow.com/a/11488902
    """
    new_args = [interval, worker_func]
    new_args.extend(args)
    threading.Timer(interval, do_every, new_args, kwargs).start()

    worker_func(*args, **kwargs)


def handshake():
    data = json.dumps({'secret': 'ILIKETURTLES'})
    r = requests.post(URL + '/api/peer', data=data, headers=json_header)
    return r.json()['id']


def request_task(_id):
    return requests.get(URL + '/api/task/request_task/' + str(_id)).json()


def send_result(answer):
    data = json.dumps(answer)
    requests.post(URL + '/api/task/send_result', data=data,
                  headers=json_header)


def send_cpu_ping(_id):
    load, own_load = get_load()

    data = json.dumps({'load': load, 'own_load': own_load})
    requests.post(URL + '/api/peer/ping/' + str(_id),
                  data=data, headers=json_header)


def get_load():
    global have_to_wait
    load = psutil.cpu_percent()
    own_load = p.cpu_percent()
    if load > 60:
        have_to_wait = True
    else:
        have_to_wait = False

    print(load, own_load)
    return load, own_load


def calculate_answer(task):
    answer = {
        'id': task['id'],
        'results': [
        ]
    }
    m_a = map(lambda x: list(map(float, x)), task['matrixA'])
    m_b = list(map(lambda x: list(map(float, x)), task['matrixB']))

    for i, r in enumerate(m_a):
        for j, c in enumerate(m_b):
            answer['results'].append({'row': i + task['start_row'],
                                      'col': j + task['start_col']})
            total = 0

            for h in range(len(r)):
                if have_to_wait:
                    print('waiting')
                    time.sleep(1)
                total += r[h] * c[h]

            answer['results'][-1]['value'] = total

    print('Finished task: ' + str(task['id']))
    return answer


if __name__ == '__main__':
    main()
