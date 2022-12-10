r = 150000000
import time 
start = time.time()

 
# iterative sum
total = 0
# iterating through 15 Million numbers
for item in range(0, r):
    total = total + item


print(total)
end = time.time()

print(end - start)


import numpy as np
import time

start = time.time()

# vectorized sum - using numpy for vectorization
# np.arange create the sequence of numbers from 0 to 1499999
print(np.sum(np.arange(r)))

end = time.time()

print(end - start)