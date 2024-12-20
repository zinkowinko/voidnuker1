from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
  app.run(host='1.1.1.1',port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()