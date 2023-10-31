import threading
import time

def hello():
    while True:
        print("hello")
        time.sleep(1)

t = threading.Thread(target=hello)

t.start()

yn = input("yes or no")    
if yn == "yes":
    t.join()

print("yay!")
