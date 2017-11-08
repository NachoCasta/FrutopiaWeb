import threading, time

def func():
    t = threading.Thread(target=hola)
    t.start()
    return

def hola():
    while True:
        print("Hola")
        time.sleep(1)

func()
