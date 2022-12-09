# from browser_history import get_history
# from datetime import datetime
# import pickle

# b_history = get_history()
# b_history = b_history.histories  # [(date/url),]
# b_history = b_history[0:3]

# # def f(param):
# #     return (datetime.timestamp(param[0]), param[1])

# f = lambda param : (datetime.timestamp(param[0]), param[1])
# a = dict(map(f, b_history))
# a = pickle.dumps(a)

# b = pickle.loads(a)
# for h in b: print(f"{datetime.fromtimestamp(h)} : {b[h]}")


# from PIL import ImageGrab

# screenshot = ImageGrab.grab()
# a = screenshot.tobytes()
# print(type(a))
# # print(a)


# save_path = os.path.join(LOCATION, f"scrn/{MAC_ADDRESS}_{self.getTS()}.jpg")
# screenshot.save(save_path)
# screenshot.show()


class Ta():
    def func_a(self):
        print('func a of test a')
    
    @staticmethod
    def func_b():
        print('func b of test a')

class Tb(Ta):
    @staticmethod
    def func_a():
        print('func a of test b')
    
class Tc(Tb):
    def func_b(self):
        print('func b of test c')

Ta().func_a()
Tb().func_a()
Tb().func_b()