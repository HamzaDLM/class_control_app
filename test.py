from browser_history import get_history
from datetime import datetime
import pickle

b_history = get_history()
b_history = b_history.histories  # [(date/url),]
b_history = b_history[0:3]

# def f(param):
#     return (datetime.timestamp(param[0]), param[1])

f = lambda param : (datetime.timestamp(param[0]), param[1])
a = dict(map(f, b_history))
a = pickle.dumps(a)

b = pickle.loads(a)
for h in b: print(f"{datetime.fromtimestamp(h)} : {b[h]}")