#!/usr/bin/env python
import random
import sys

size = int(sys.argv[1])

random_matrix = [[str(random.random()) for i in range(size)] for j in
                 range(size)]

random_matrix = map(lambda r: ' '.join(r), random_matrix)
random_matrix = '\n'.join(random_matrix)

f = open(sys.argv[2], 'w')
f.write(random_matrix)
