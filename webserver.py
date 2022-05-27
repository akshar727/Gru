from flask import Flask

from threading import Thread



app = Flask('')



@app.route('/')

def home():

    return "Discord bot is OK and running\nWebserver is OK and ready to be pinged!"



def run():
  app.run(host='0.0.0.0',port=8080)


def keep_alive():  

    t = Thread(target=run)

    t.start()