#!/usr/bin/env python
from pprint import pprint
import requests
import json

URL = 'http://localhost:5000'
json_header = {'content-type': 'application/json'}

"""
task = {
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
"""

def main():
    _id = handshake()
    print(_id)

    task = request_task(_id)




def handshake():
    data = json.dumps({'secret': 'BILIKETURTLES'})
    r = requests.post(URL + '/api/peer', data=data, headers=json_header)
    return r.json()['id']

def request_task(_id):
    return requests.get(URL + '/api/request_task')


def calculate_answer(task):
    answer = {
        'id': task['id'],
        'results': [
        ]
    }

    for r in task['rows']:
        for c in task['columns']:
            answer['results'].append({'row': r['number'], 'col': c['number']})
            total = 0

            for i in range(len(r['sequence'])):
                total += r['sequence'][i] * c['sequence'][i]

            answer['results'][-1]['value'] = total

    pprint(answer)
    return answer


if __name__ == '__main__':
    main()
