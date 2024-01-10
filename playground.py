
class Hoge:
    def __init__(self):
        self.func = lambda: None
        self.trigger = lambda: self.func()



def hello():
    print('hello')

hoge = Hoge()
hoge.func = hello
hoge.trigger()
