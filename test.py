fps = []
import random
import string
import os
import time
letters = string.ascii_lowercase

start = time.time()
names = []
for i in range(10000):
    name = ''.join(random.choice(letters) for i in range(10))
    file = os.path.join('temp', name)
    names.append(file)
end = time.time()
print(end - start)

start = time.time()
for name in names:  
    fp = open(name, 'w')
end = time.time()
print(end - start)