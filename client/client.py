#!/usr/bin/env python
from pprint import pprint

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
